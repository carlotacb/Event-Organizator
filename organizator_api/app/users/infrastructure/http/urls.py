from django.urls import path

from app.users.infrastructure.http.views import (
    create_new_user,
    get_all_users,
    get_user_by_id,
    get_user_by_username,
    update_user,
)

urlpatterns = [
    path("new", create_new_user),
    path("", get_all_users),
    path("<uuid:user_id>", get_user_by_id),
    path("<str:username>", get_user_by_username),
    path("update/<uuid:user_id>", update_user),
]
