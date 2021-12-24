from django.urls import path
from domain import views


urlpatterns = [
    path("solve", views.domain_solve, name="domain_solve"),
    path("<domain_id>", views.domain, name="domain"),
]
