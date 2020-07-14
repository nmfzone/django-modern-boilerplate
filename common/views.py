import pydash
from django.contrib import messages
from django.contrib.auth import (
    login as auth_login, logout as auth_logout,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import SuccessURLAllowedHostsMixin
from django.http import Http404, HttpResponseForbidden, JsonResponse
from django.shortcuts import resolve_url
from django.utils.decorators import method_decorator
from django.utils.http import is_safe_url
from django.views import generic
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import edit
from django.views.generic.base import View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import DeletionMixin
from .forms import AuthenticationForm
from .mixins.redirector import RedirectorMixin
from .mixins.validator import ValidatorMixin
from .paginator import Paginator
from .queue import QueueManager


class RetryQueueView(LoginRequiredMixin, generic.View):
    http_method_names = ['get']

    def get(self, request, task_id):
        queue = QueueManager()
        result = queue.retry_queue(task_id)

        if result['status'] == 'Found':
            return JsonResponse({
                'data': result['data']
            })
        elif result['status'] == 'Forbidden':
            return HttpResponseForbidden(result['message'])

        raise Http404(result['message'])


class LoginView(SuccessURLAllowedHostsMixin, ValidatorMixin, RedirectorMixin, edit.FormView):
    template_name = 'common:auth/login.html'
    form_class = AuthenticationForm
    success_url = 'dashboard'
    page_title = 'Login'
    redirect_field_name = 'next'
    redirect_authenticated_user = True

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if self.redirect_authenticated_user and self.request.user.is_authenticated:
            redirect_to = self.get_success_url()
            if redirect_to == self.request.path:
                raise ValueError(
                    "Redirection loop for authenticated user detected. Ensure that "
                    "your success_url doesn't point to a login page."
                )
            return self.redirector().to(redirect_to)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        auth_login(self.request, form.get_user())

        return self.redirector().to(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            self.redirect_field_name: self.get_redirect_url(),
            'page_title_': self.page_title,
        })

        return context

    def get_success_url(self):
        url = self.get_redirect_url()

        return url or resolve_url(self.success_url)

    def get_redirect_url(self):
        redirect_to = self.request.POST.get(
            self.redirect_field_name,
            self.request.GET.get(self.redirect_field_name, '')
        )
        url_is_safe = is_safe_url(
            url=redirect_to,
            allowed_hosts=self.get_success_url_allowed_hosts(),
            require_https=self.request.is_secure(),
        )

        return redirect_to if url_is_safe else ''


class LogoutView(RedirectorMixin, generic.View):
    http_method_names = ['post']

    def post(self, request):
        if not request.user:
            return self.redirector().to('/')

        auth_logout(request)

        return self.redirector().to('/')


class ListView(RedirectorMixin, generic.ListView):
    paginator_class = Paginator
    page_title = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title_': self.page_title,
        })

        return context

    def get_paginator(self, queryset, per_page, orphans=0,
                      allow_empty_first_page=True, **kwargs):
        paginator_class = self.paginator_class(
            queryset, per_page, orphans,
            allow_empty_first_page
        )
        setattr(paginator_class, 'current_page', self.get_current_page())

        return paginator_class

    def get_current_page(self):
        page = self.kwargs.get(self.page_kwarg) or self.request.GET.get(self.page_kwarg) or 1

        try:
            page = int(page)
        except ValueError:
            page = 1

        return page


class CreateView(ValidatorMixin, RedirectorMixin, edit.CreateView):
    page_title = None
    success_message = 'Created successfully.'

    def form_valid(self, form):
        self.object = form.save()

        success_message = self.get_success_message(form.cleaned_data)
        if success_message:
            messages.success(self.request, success_message)

        return self.redirector().to(self.get_success_url())

    def get_success_message(self, cleaned_data):
        return self.success_message % cleaned_data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title_': self.page_title,
        })

        return context


class DetailView(ValidatorMixin, RedirectorMixin, generic.DetailView):
    page_title = None
    title_field = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title_': pydash.get(self.object, self.title_field, self.page_title),
        })

        return context


class EditView(ValidatorMixin, RedirectorMixin, edit.UpdateView):
    http_method_names = ['get', 'put']
    page_title = None
    success_message = 'Updated successfully.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title_': self.page_title,
        })

        return context

    def form_valid(self, form):
        self.object = form.save()

        success_message = self.get_success_message(form.cleaned_data)
        if success_message:
            messages.success(self.request, success_message)

        return self.redirector().to(self.get_success_url())

    def get_success_message(self, cleaned_data):
        return self.success_message % cleaned_data

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        if self.request.original_method == 'POST':
            kwargs.update({
                'data': self.request.INPUT,
                'files': self.request.FILES,
            })

        return kwargs


class DeleteView(DeletionMixin, RedirectorMixin, SingleObjectMixin, View):
    http_method_names = ['delete']
    success_message = 'Deleted sucessfully.'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()

        if self.success_message:
            messages.success(self.request, self.success_message)

        return self.redirector().to(success_url)


class TemplateView(RedirectorMixin, generic.TemplateView):
    page_title = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title_': self.page_title,
        })

        return context
