from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    # path('protected/admin/', admin.site.urls),
    path('', include('common.urls')),
    path('', include('app.urls')),
    # path('oauth/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]

urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + urlpatterns

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
