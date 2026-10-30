"""URL configuration for UGHE Test Web App backend."""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path, re_path
from django.views.static import serve


def health_check(request):
    return JsonResponse({'status': 'ok', 'service': 'ughe-backend'})


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/health/', health_check, name='health'),
    path('api/auth/', include('accounts.urls')),
    path('api/content/', include('content.urls')),
    # Always serve uploaded media (assessment / Docker convenience)
    re_path(
        r'^media/(?P<path>.*)$',
        serve,
        {'document_root': settings.MEDIA_ROOT},
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

admin.site.site_header = 'UGHE Test Web App Administration'
admin.site.site_title = 'UGHE Admin'
admin.site.index_title = 'Website Content Management'
