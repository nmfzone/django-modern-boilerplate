from common.http.redirector import HttpRedirector


class RedirectorMixin:
    def redirector(self):
        # @TODO: We may changed this to getter
        return HttpRedirector(self.request)

    def back(self, fallback='/'):
        return self.redirector().back(fallback)
