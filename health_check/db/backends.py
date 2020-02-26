from django.db import DatabaseError, IntegrityError

from health_check.backends import BaseHealthCheckBackend
from health_check.exceptions import (
    ServiceReturnedUnexpectedResult, ServiceUnavailable
)

from .models import TestModel


class DatabaseBackend(BaseHealthCheckBackend):
    """Health check for DatabaseBackend."""

    def check_status(self):
        """Check django database creating an object on the db, update and delete it."""
        try:
            obj = TestModel.objects.create(title="test")
            obj.title = "newtest"
            obj.save()
            obj.delete()

        except IntegrityError as e:
            self.add_error(ServiceReturnedUnexpectedResult("Integrity Error"), e)

        except DatabaseError as e:
            self.add_error(ServiceUnavailable("Database error"), e)
