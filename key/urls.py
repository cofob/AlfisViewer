from django.urls import path
from key import views


urlpatterns = [
    path("<key_id>", views.key, name="key"),
]
