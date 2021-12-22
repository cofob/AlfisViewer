from django.urls import path
from solver import views


urlpatterns = [
    path("", views.index),
]
