from django.urls import path

from app.users.infrastructure.http.views import create_new_user

urlpatterns = [
    path("new", create_new_user),
]
