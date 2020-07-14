from common.models import User
from common.tasks import send_registration_email_task
from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm as BaseAuthenticationForm,
    ReadOnlyPasswordHashField
)
from django.utils.translation import gettext as _


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'name')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("The password confirmation does not match.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()
            send_registration_email_task.delay(
                self.cleaned_data['email'],
                _('Welcome to the Nmfblog.')
            )

        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'name', 'is_admin')

    def clean_password(self):
        return self.initial["password"]


class AuthenticationForm(BaseAuthenticationForm):
    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
