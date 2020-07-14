import pydash as _
from common.exceptions import FormErrorBag
from django.http import HttpResponseRedirect as BaseHttpResponseRedirect
from querystring_parser import parser


class HttpRedirector:
    def __init__(self, request):
        self.request = request

    def to(self, path):
        return HttpResponseRedirect(path).set_request(self.request)

    def back(self, fallback='/'):
        previous_url = self.request.META.get('HTTP_REFERER', self.request.session.get('_previous.url', fallback))

        return self.to(previous_url)


class HttpResponseRedirect(BaseHttpResponseRedirect):
    request = None

    def with_errors(self, errors):
        self.request.session['_errors'] = FormErrorBag(errors).serialize()
        return self

    def with_input(self, data=None):
        if not data:
            data = _.merge(parser.parse(self.request.GET.urlencode()), parser.parse(self.request.POST.urlencode()))

        self.request.session['_old_input'] = _.omit(data, ['csrfmiddlewaretoken'])
        return self

    def set_request(self, request):
        self.request = request
        return self
