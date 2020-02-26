from django.utils.translation import gettext_lazy as _  # noqa: N812


class HealthCheckException(Exception):
    """
    Base health check exception.

    This error is handled by default as a Service Unknown Error.
    To handle a specific error, inherit this class and create a new excpetion.
    """
    message_type = _("Service unknown error")

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return "%s: %s" % (self.message_type, self.message)


class ServiceWarning(HealthCheckException):
    """
    Warning of service misbehavior.

    If the ``HEALTH_CHECK['WARNINGS_AS_ERRORS']`` is set to ``False``,
    these exceptions will not case a 500 status response.
    """

    message_type = _("Service Warning")


class ServiceUnavailable(HealthCheckException):
    """Exception that handles service unavailable error."""
    message_type = _("Service unavailable")


class ServiceReturnedUnexpectedResult(HealthCheckException):
    """Exception that handles service returned unexpected result error."""
    message_type = _("Service returned unexpected result")
