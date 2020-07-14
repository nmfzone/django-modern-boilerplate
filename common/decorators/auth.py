from functools import wraps
from urllib.parse import urlparse
from common.exceptions import AuthenticationException
from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import resolve_url


def user_passes_test(test_func, login_url=None, redirect_field_name=REDIRECT_FIELD_NAME):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if test_func(request.user):
                return view_func(request, *args, **kwargs)
            path = request.build_absolute_uri()
            resolved_login_url = resolve_url(login_url or settings.LOGIN_URL)

            login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
            current_scheme, current_netloc = urlparse(path)[:2]

            if (
                (not login_scheme or login_scheme == current_scheme) and
                (not login_netloc or login_netloc == current_netloc)
            ):
                path = request.get_full_path()

            if request.match('api/*'):
                raise AuthenticationException()

            return redirect_to_login(
                path,
                resolved_login_url,
                redirect_field_name
            )

        return _wrapped_view

    return decorator


def login_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
