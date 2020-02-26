import copy

from concurrent.futures import ThreadPoolExecutor

from django.db import connection

from health_check.settings import HEALTH_CHECK
from health_check.exceptions import ServiceWarning
from health_check.plugins import plugin_dir


class CheckMixin:
    _errors = None
    _plugins = None

    @property
    def plugins_check(self):
        return self._errors if self._errors else self.run_check()

    @property
    def plugins(self):
        if not self._plugins:
            self._plugins = sorted((
                plugin_class(**copy.deepcopy(options))
                for plugin_class, options in plugin_dir._registry
            ), key=lambda plugin: plugin.identifier())
        return self._plugins

    def run_check(self):
        errors = []

        def _run(plugin):
            plugin.run_check()
            try:
                return plugin
            finally:
                connection.close()

        with ThreadPoolExecutor(max_workers=len(self.plugins) or 1) as executor:
            for plugin in executor.map(_run, self.plugins):
                if plugin.critical_service:
                    if not HEALTH_CHECK['WARNINGS_AS_ERRORS']:
                        errors.extend(
                            e for e in plugin.errors
                            if not isinstance(e, ServiceWarning)
                        )
                    else:
                        errors.extend(plugin.errors)

        return errors
