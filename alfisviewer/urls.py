"""alfisviewer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.http.response import FileResponse

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("index.urls")),
    path("block/", include("block.urls")),
    path("search/", include("search.urls")),
    path("domain/", include("domain.urls")),
    path("key/", include("key.urls")),
    path("blockchain.db", lambda x: FileResponse(x, filename="blockchain.db")),
    path("db.sqlite3", lambda x: FileResponse(x, filename="db.sqlite3")),
]

if settings.DEBUG:
    urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

admin.site.site_header = "AlfisViewer admin" + (" debug" if settings.DEBUG else "")
admin.site.site_title = "AlfisViewer admin" + (" debug" if settings.DEBUG else "")
