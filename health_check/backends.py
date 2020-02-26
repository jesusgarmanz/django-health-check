import logging

from timeit import default_timer as timer

from django.utils.translation import gettext_lazy as _  # noqa: N812

from health_check.exceptions import (
    HealthCheckException, ServiceUnavailable
)

logger = logging.getLogger('health-check')


class BaseHealthCheckBackend:
    """
    Django base health check backend.

    This class handles the checker logic for the plugins: run the plugins health checks,
    manage a list of errors that happened during checks and handles the representation
    of the plugin status returned to the view.

    Attributes:
        critical_service(bool): Define if service is critical to the operation of the site.
            If set to ``True`` service failures return 500 response code on the
            health check endpoint.
    """

    critical_service = True

    def __init__(self):
        """Instance method."""

        self.errors = []

    def check_status(self):
        raise NotImplementedError

    def run_check(self):
        """
        Function that call plugin ``check_status`` own method,
        handles the exceptions that could happend during the ``check_status`` and
        calculate check execution time.

        Returns:
            None
        """

        start = timer()
        self.errors = []
        try:
            self.check_status()
        except HealthCheckException as e:
            self.add_error(e, e)
        except NotImplementedError:
            logger.exception('Method not implemented')
            raise
        except BaseException as e:
            logger.exception("Unexpected Error!")
            self.add_error(ServiceUnavailable("Service unknown error"), e)
        finally:
            self.time_taken = timer() - start

    def add_error(self, error, cause=None):
        """
        Function that checks the type of exception and append into the registry of errors.
        The management of the exception depends of the type of the exception as well as the
        message of the excpeiton.

        Args:
            error (obj): Exception object.
            cause (:obj, optional): Exception object to handle logger level.
        Returns:
            None
        """
        if isinstance(error, HealthCheckException):
            pass
        elif isinstance(error, str):
            msg = error
            error = HealthCheckException(msg)
        else:
            msg = _("unknown error")
            error = HealthCheckException(msg)
        if isinstance(cause, BaseException):
            logger.exception(str(error))
        else:
            logger.error(str(error))
        self.errors.append(error)

    def pretty_status(self):
        """Function that handles the representation of the status of the plugin."""
        if self.errors:
            return "\n".join(str(e) for e in self.errors)
        return _('working')

    @property
    def status(self):
        return int(not self.errors)

    def identifier(self):
        return self.__class__.__name__
