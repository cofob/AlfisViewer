from django.urls import path
from domain import views


urlpatterns = [
    path("", views.domain_list, name="domain_list"),
    path("solve", views.domain_solve, name="domain_solve"),
    path("<domain_id>", views.domain, name="domain"),
    path("<domain_id>/history", views.domain_history, name="domain_history"),
]
