"""URL configuration for UGHE Test Web App backend."""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import HttpResponse, JsonResponse
from django.urls import include, path, re_path
from django.views.static import serve


def health_check(request):
    return JsonResponse({'status': 'ok', 'service': 'ughe-backend'})


def api_root(request):
    """Friendly landing page for http://localhost:8000/"""
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="utf-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1" />
      <title>UGHE Backend API</title>
      <style>
        body { font-family: Georgia, serif; max-width: 720px; margin: 48px auto; padding: 0 20px; color: #222; }
        h1 { color: #BE1E2D; }
        a { color: #BE1E2D; }
        code { background: #f4f4f4; padding: 2px 6px; }
        ul { line-height: 1.8; }
        .note { background: #f8e9ea; border-left: 4px solid #BE1E2D; padding: 12px 16px; margin-top: 24px; }
      </style>
    </head>
    <body>
      <h1>UGHE Test Web App — Backend</h1>
      <p>Django REST API is running. This is not the public website UI.</p>
      <p>Use the Next.js frontend at <a href="http://localhost:3000">http://localhost:3000</a>.</p>

      <h2>Useful links</h2>
      <ul>
        <li><a href="/admin/">Django Admin</a> — manage website content</li>
        <li><a href="/api/health/">Health check</a></li>
        <li><code>POST /api/auth/login/</code></li>
        <li><code>GET /api/content/navigation/</code> (JWT required)</li>
        <li><code>GET /api/content/slides/</code> (JWT required)</li>
        <li><code>GET /api/content/statistics/</code> (JWT required)</li>
        <li><code>GET /api/content/sections/</code> (JWT required)</li>
        <li><code>GET /api/content/settings/</code> (JWT required)</li>
      </ul>

      <div class="note">
        <strong>Admin login:</strong> username <code>admin</code> /
        password <code>UgheAdmin2024!</code>
      </div>
    </body>
    </html>
    """
    return HttpResponse(html)


urlpatterns = [
    path('', api_root, name='api-root'),
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
