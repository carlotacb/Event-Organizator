from django.urls import path

from app.users.infrastructure.http.views import create_new_user, get_all_users

urlpatterns = [
    path("new", create_new_user),
    path("", get_all_users),
]
