from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from .utils import serve_file
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("index.urls")),
    path("block/", include("block.urls")),
    path("search/", include("search.urls")),
    path("domain/", include("domain.urls")),
    path("key/", include("key.urls")),
    path("settings/", include("settings_app.urls")),
    path(
        "blockchain.db",
        serve_file("blockchain.db", "application/x-sqlite3"),
        name="blockchain",
    ),
    path("favicon.ico", serve_file("favicon.ico", "image/x-icon")),
]

if settings.DEBUG:
    urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

admin.site.site_header = "AlfisViewer admin" + (" debug" if settings.DEBUG else "")
admin.site.site_title = "AlfisViewer admin" + (" debug" if settings.DEBUG else "")

handler404 = "alfisviewer.views.handler404"
handler500 = "alfisviewer.views.handler500"
