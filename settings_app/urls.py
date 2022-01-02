from django.urls import path
from settings_app import views


urlpatterns = [
    path("", views.index, name="settings"),
]
