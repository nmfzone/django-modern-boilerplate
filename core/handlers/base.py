import logging
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured, MiddlewareNotUsed
from django.utils.module_loading import import_string
from .exception import patched_convert_exception_to_response


def patched_load_middleware(self):
    logger = logging.getLogger('django.request')

    self._view_middleware = []
    self._template_response_middleware = []
    self._exception_middleware = []

    handler = patched_convert_exception_to_response(self._get_response)
    for middleware_path in reversed(settings.MIDDLEWARE):
        middleware = import_string(middleware_path)
        try:
            mw_instance = middleware(handler)
        except MiddlewareNotUsed as exc:
            if settings.DEBUG:
                if str(exc):
                    logger.debug('MiddlewareNotUsed(%r): %s', middleware_path, exc)
                else:
                    logger.debug('MiddlewareNotUsed: %r', middleware_path)
            continue

        if mw_instance is None:
            raise ImproperlyConfigured(
                'Middleware factory %s returned None.' % middleware_path
            )

        if hasattr(mw_instance, 'process_view'):
            self._view_middleware.insert(0, mw_instance.process_view)
        if hasattr(mw_instance, 'process_template_response'):
            self._template_response_middleware.append(mw_instance.process_template_response)
        if hasattr(mw_instance, 'process_exception'):
            self._exception_middleware.append(mw_instance.process_exception)

        handler = patched_convert_exception_to_response(mw_instance)

    self._middleware_chain = handler
