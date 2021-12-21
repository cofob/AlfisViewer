from django.urls import path
from block import views


urlpatterns = [
    path("<block_id>", views.block, name="block"),
]
