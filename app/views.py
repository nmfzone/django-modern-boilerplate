from common.views import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class IndexView(TemplateView):
    template_name = 'app:index.html'
    page_title = 'Django Boilerplate'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'app:dashboard.html'
    page_title = 'Dashboard'
