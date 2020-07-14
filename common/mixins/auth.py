from common.exceptions import AuthenticationException
from django.contrib.auth.mixins import LoginRequiredMixin as BaseLoginRequiredMixin
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied


class LoginRequiredMixin(BaseLoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def handle_no_permission(self):
        if self.raise_exception or self.request.user.is_authenticated:
            raise PermissionDenied(self.get_permission_denied_message())

        if self.request.match('api/*'):
            raise AuthenticationException()

        return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())
