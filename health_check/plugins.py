class AlreadyRegistered(Exception):
    pass


class NotRegistered(Exception):
    pass


class HealthCheckPluginDirectory:
    """
    Django health check registry.

    This class defines the plugins to be checked in the django application.
    """

    def __init__(self):
        self._registry = []  # plugin_class class -> plugin options

    def reset(self):
        """Reset registry state, e.g. for testing purposes."""
        self._registry = []

    def register(self, plugin, **options):
        """
        Add the given plugin to the registry.

        Instantiate the admin class to save in the registry.
        """
        self._registry.append((plugin, options))


plugin_dir = HealthCheckPluginDirectory()
