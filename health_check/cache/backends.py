import logging

from django.core.cache import CacheKeyWarning, cache

from health_check.backends import BaseHealthCheckBackend
from health_check.exceptions import (
    ServiceReturnedUnexpectedResult, ServiceUnavailable
)

logger = logging.getLogger(__name__)


class CacheBackend(BaseHealthCheckBackend):
    def check_status(self):
        try:
            key = 'djangohealtcheck_test'
            value = 'itworks'

            logger.debug(f"Storing on cache key-value pair: {key}-{value} .")
            cache.set(key, value, 1)

            logger.debug('Key-value pair stored on cache. Attemtping to retrieve it...')
            cache.set('djangohealtcheck_test', 'itworks', 1)
            if not cache.get("djangohealtcheck_test") == "itworks":
                self.add_error(ServiceReturnedUnexpectedResult("Cache key does not match"))
        except CacheKeyWarning as e:
            self.add_error(ServiceReturnedUnexpectedResult("Cache key warning"), e)
        except ValueError as e:
            self.add_error(ServiceReturnedUnexpectedResult("ValueError"), e)
        except ConnectionError as e:
            self.add_error(ServiceReturnedUnexpectedResult("Connection Error"), e)
        except BaseException as e:
            self.add_error(ServiceUnavailable("Unknown error"), e)
