from django.urls import path
from domain import views


urlpatterns = [
    path("<domain_id>", views.domain, name="block"),
]
