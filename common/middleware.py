import pydash
from common.http.files import transform_uploaded_files
from common.utils import service_provider
from django.conf import settings


class HandleValidationErrorsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if response.status_code != 302:
            def remove_session(key):
                try:
                    del request.session[key]
                except KeyError:
                    pass

            pydash.for_each(['_old_input', '_errors'], remove_session)

        return response


class PreviousUrlMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'GET' and not request.is_ajax():
            request.session['_previous.url'] = request.get_full_path()

        response = self.get_response(request)

        return response


class HttpRequestPatchMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.method == 'POST':
            method_override = self._get_method_override(request)

            if method_override in ['PUT', 'PATCH', 'DELETE']:
                request.method = method_override

    def _get_method_override(self, request):
        method = (
            request.POST.get('_method') or
            request.META.get('HTTP_X_HTTP_METHOD_OVERRIDE')
        )
        return method and method.upper()

    def __call__(self, request):
        request.original_method = request.method

        if request.method == 'GET':
            request.INPUT = request.GET.copy()

        if request.method == 'POST':
            data = request.POST.copy()

            for key, value in request.GET.copy().lists():
                if key not in data:
                    data.setlist(key, value)

            request.INPUT = data

        request._files = transform_uploaded_files(request.FILES)
        # idk it's bad or not (https://stackoverflow.com/q/19581110/4484016)
        # at least, it works :)
        request._read_started = False

        return self.get_response(request)


class ServiceProviderMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        service_provider.instance('request', request)
        return self.get_response(request)


def show_toolbar(request):
    return settings.DEBUG and not settings.DISABLE_DEBUG_TOOLBAR
