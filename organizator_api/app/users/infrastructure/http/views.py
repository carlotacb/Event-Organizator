import json
import uuid

from django.http import HttpRequest, HttpResponse
from django.views.decorators.http import require_http_methods

from app.users.application.requests import CreateUserRequest, UpdateUserRequest
from app.users.application.response import UserResponse
from app.users.domain.exceptions import UserAlreadyExists, UserNotFound, InvalidPassword
from app.users.domain.usecases.create_user_use_case import CreateUserUseCase
from app.users.domain.usecases.get_all_users_use_case import GetAllUsersUseCase
from app.users.domain.usecases.get_user_by_id_use_case import GetUserByIdUseCase
from app.users.domain.usecases.get_user_by_username_use_case import (
    GetUserByUsernameUseCase,
)
from app.users.domain.usecases.login_use_case import LoginUseCase
from app.users.domain.usecases.update_user_use_case import UpdateUserUseCase


@require_http_methods(["POST"])
def create_new_user(request: HttpRequest) -> HttpResponse:
    json_body = json.loads(request.body)

    try:
        email = json_body["email"]
        password = json_body["password"]
        first_name = json_body["first_name"]
        last_name = json_body["last_name"]
        username = json_body["username"]
        bio = json_body["bio"]
        profile_image = json_body["profile_image"]
    except (TypeError, KeyError):
        return HttpResponse(status=400, content="Unexpected body")

    user_data = CreateUserRequest(
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
        username=username,
        bio=bio,
        profile_image=profile_image,
    )

    try:
        CreateUserUseCase().execute(user_data)
    except UserAlreadyExists:
        return HttpResponse(status=409, content="User already exists")

    return HttpResponse(status=201, content="User created correctly")


@require_http_methods(["GET"])
def get_all_users(request: HttpRequest) -> HttpResponse:
    all_users = GetAllUsersUseCase().execute()

    users_response = []
    for user in all_users:
        users_response.append(UserResponse.from_user(user).to_dict())

    return HttpResponse(
        status=200, content=json.dumps(users_response), content_type="application/json"
    )


@require_http_methods(["GET"])
def get_user_by_id(request: HttpRequest, user_id: uuid.UUID) -> HttpResponse:
    try:
        user = GetUserByIdUseCase().execute(user_id=user_id)
    except UserNotFound:
        return HttpResponse(status=404, content="User does not exist")

    return HttpResponse(
        status=200,
        content=json.dumps(UserResponse.from_user(user).to_dict()),
        content_type="application/json",
    )


@require_http_methods(["GET"])
def get_user_by_username(request: HttpRequest, username: str) -> HttpResponse:
    try:
        user = GetUserByUsernameUseCase().execute(username=username)
    except UserNotFound:
        return HttpResponse(status=404, content="User does not exist")

    return HttpResponse(
        status=200,
        content=json.dumps(UserResponse.from_user(user).to_dict()),
        content_type="application/json",
    )


@require_http_methods(["POST"])
def update_user(request: HttpRequest, user_id: uuid.UUID) -> HttpResponse:
    json_body = json.loads(request.body)

    if "email" in json_body:
        return HttpResponse(status=400, content="The email cannot be updated")
    if "password" in json_body:
        return HttpResponse(status=400, content="The password cannot be updated")

    username = json_body["username"] if "username" in json_body else None
    first_name = json_body["first_name"] if "first_name" in json_body else None
    last_name = json_body["last_name"] if "last_name" in json_body else None
    bio = json_body["bio"] if "bio" in json_body else None
    profile_image = json_body["profile_image"] if "profile_image" in json_body else None

    user_data = UpdateUserRequest(
        username=username,
        first_name=first_name,
        last_name=last_name,
        bio=bio,
        profile_image=profile_image,
    )

    try:
        user = UpdateUserUseCase().execute(user_id=user_id, user=user_data)
    except UserNotFound:
        return HttpResponse(status=404, content="User does not exist")
    except UserAlreadyExists:
        return HttpResponse(status=409, content="User already exists")

    return HttpResponse(
        status=200,
        content=json.dumps(UserResponse.from_user(user).to_dict()),
        content_type="application/json",
    )


@require_http_methods(["POST"])
def login_user(request: HttpRequest) -> HttpResponse:
    json_body = json.loads(request.body)

    if "username" not in json_body:
        return HttpResponse(status=400, content="Username is required")
    if "password" not in json_body:
        return HttpResponse(status=400, content="Password is required")

    username = json_body["username"]
    password = json_body["password"]

    try:
        token = LoginUseCase().execute(username=username, password=password)
    except UserNotFound:
        return HttpResponse(status=404, content="User does not exist")
    except InvalidPassword:
        return HttpResponse(status=401, content="Invalid password")

    return HttpResponse(
        status=200,
        content=json.dumps({"token": str(token)}),
        content_type="application/json",
    )
