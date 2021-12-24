from django.urls import path
from block import views


urlpatterns = [
    path("", views.block_list, name="block_list"),
    path("<block_id>", views.block, name="block"),
]
