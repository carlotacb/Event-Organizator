from django.urls import path

from app.users.infrastructure.http.views import (
    create_new_user,
    get_all_users,
    get_user_by_id,
    get_user_by_username,
    update_my_user,
    login,
    get_user_by_token,
    logout,
    get_role_by_token,
    update_role,
)

urlpatterns = [
    path("new", create_new_user),
    path("", get_all_users),
    path("me", get_user_by_token),
    path("me/role", get_role_by_token),
    path("login", login),
    path("logout", logout),
    path("update/role/<uuid:user_id>", update_role),
    path("update/me", update_my_user),
    path("<uuid:user_id>", get_user_by_id),
    path("<str:username>", get_user_by_username),
]
