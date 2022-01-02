from django.urls import path
from settings_app import views


urlpatterns = [
    path("", views.index, name="settings"),
    path("set_lang/<lang_code>", views.set_lang, name="set_lang"),
]
