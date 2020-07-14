import pydash
from common.exceptions import AuthenticationException, BadRequest
from common.http.redirector import HttpRedirector
from django.conf import settings
from django.core.exceptions import ValidationError, PermissionDenied
from django.core.handlers.exception import (
    response_for_exception as base_response_for_exception
)
from django.http import JsonResponse, Http404
from django.utils.translation import gettext as _
from functools import wraps
from querystring_parser import parser
from requests import status_codes


def response_for_exception(request, exception):
    response = base_response_for_exception(request, exception)

    if isinstance(exception, ValidationError):
        dont_flash = [
            'password',
            'password_confirmation',
        ]

        old_input = pydash.merge(parser.parse(request.GET.urlencode()), parser.parse(request.POST.urlencode()))
        errors = exception.message_dict if hasattr(exception, 'error_dict') else {'__all__': exception.messages}

        response = HttpRedirector(request) \
            .back() \
            .with_input(pydash.omit(old_input, dont_flash)) \
            .with_errors(errors)

    if request.match('api/*') and not isinstance(response, JsonResponse):
        message = str(exception)
        data = {}

        if isinstance(exception, ValidationError):
            status_code = 422
            message = _('Invalid data!')
            data['errors'] = exception.message_dict if hasattr(exception, 'error_dict') else {'__all__': exception.messages}
        elif isinstance(exception, Http404):
            status_code = 404
        elif isinstance(exception, BadRequest):
            status_code = 400
        elif isinstance(exception, AuthenticationException):
            status_code = 401
        elif isinstance(exception, PermissionDenied):
            status_code = 403
        else:
            status_code = 500

            if not settings.DEBUG:
                message = _('Something went wrong')

        if len(message.strip()) == 0:
            message = _(status_codes._codes[status_code][0])

        return JsonResponse(pydash.merge({
            'message': message
        }, data), status=status_code)

    return response


def patched_convert_exception_to_response(get_response):
    @wraps(get_response)
    def inner(request):
        try:
            response = get_response(request)
        except Exception as exc:
            response = response_for_exception(request, exc)
        return response

    return inner
