import pydash
import re
from common.utils import Str
from django.http import HttpRequest
from django_user_agents.utils import get_user_agent
from django_accept_header.header import parse as parse_accept_header
from functools import wraps
from ipware import get_client_ip
from urllib.parse import urlsplit


def add_method(cls):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            return func(self, *args, **kwargs)

        setattr(cls, func.__name__, wrapper)
        return func

    return decorator


def override_method(cls, after=True):
    def decorator(func):
        new_parent_method_name = '_' + func.__name__ + '_parent'
        setattr(cls, new_parent_method_name, getattr(cls, func.__name__))

        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if after:
                parent_result = getattr(self, new_parent_method_name)(*args, **kwargs)
                return func(self, parent_result, *args, **kwargs)
            elif after == False:
                func(self, *args, **kwargs)
                return getattr(self, new_parent_method_name)(*args, **kwargs)

            return func(self, *args, **kwargs)

        setattr(cls, func.__name__, wrapper)
        return func

    return decorator


def add_property(cls):
    def decorator(func):
        setattr(cls, func.__name__, property(func))
        return func

    return decorator


@add_method(HttpRequest)
def match(self, *patterns):
    current_url = pydash.replace_start(urlsplit('//%s' % self.get_full_path()).path, '/', '')

    if current_url == '':
        current_url = '/'

    for pattern in patterns:
        pattern = pattern.replace('*', '.*')
        pattern = '^' + pattern + '$'

        if not re.match(pattern, current_url):
            return False

    return True


@add_property(HttpRequest)
def ip(self):
    client_ip, is_routable = get_client_ip(self)
    return client_ip


@add_property(HttpRequest)
def user_agent(self):
    return get_user_agent(self)


@add_property(HttpRequest)
def prefetch(self):
    return 'prefetch' in self.META.get('HTTP_X_MOZ', '').lower() or \
           'prefetch' in self.META.get('HTTP_Purpose', '').lower()


@add_property(HttpRequest)
def pjax(self):
    if self.META.get('X-PJAX'):
        return True
    return False


@add_method(HttpRequest)
def accepts(self, content_types):
    acceptable_types = self.get_acceptable_types

    return any(acceptable_type.matches(content_types) for acceptable_type in acceptable_types)


@add_property(HttpRequest)
def accepts_json(self):
    return self.accepts('application/json')


@add_property(HttpRequest)
def expects_json(self):
    return (self.is_ajax() and not self.pjax and self.accepts_any_content_type) or self.wants_json


@add_property(HttpRequest)
def wants_json(self):
    acceptable_types = self.get_acceptable_types

    return len(acceptable_types) >= 0 and Str.contains(acceptable_types[0], ['/json', '+json'])


@add_property(HttpRequest)
def accepts_any_content_type(self):
    acceptable_types = self.get_acceptable_types

    return len(acceptable_types) == 0 or \
        (len(acceptable_types) >= 0 and (acceptable_types[0] == '*/*' or acceptable_types[0] == '*'))


@add_property(HttpRequest)
def get_acceptable_types(self):
    if not hasattr(self, 'acceptable_types'):
        self.acceptable_types = parse_accept_header(self.META.get('HTTP_ACCEPT', ''))

    return self.acceptable_types
