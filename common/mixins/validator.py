from django.core.exceptions import ValidationError


class ValidatorMixin:
    def form_invalid(self, form):
        raise ValidationError(form.errors)
