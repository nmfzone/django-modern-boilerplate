from django.conf import settings


def settings_context_processor(request):
    return {
        'APP_VERSION': settings.APP_VERSION,
        'APP_NAME': settings.APP_NAME,
    }
