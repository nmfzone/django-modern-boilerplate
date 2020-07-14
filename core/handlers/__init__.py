from core.handlers.base import patched_load_middleware
from django.core.handlers.base import BaseHandler


BaseHandler.load_middleware = patched_load_middleware
