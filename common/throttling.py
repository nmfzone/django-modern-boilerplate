from django.conf import settings
from rest_framework.throttling import (
    ScopedRateThrottle as BaseScopedRateThrottle
)


class ScopedRateThrottle(BaseScopedRateThrottle):
    def allow_request(self, request, view):
        if settings.DEBUG:
            setattr(view, self.scope_attr, 'debug')

        return super().allow_request(request, view)
