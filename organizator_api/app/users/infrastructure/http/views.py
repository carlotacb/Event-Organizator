import json

from django.http import HttpRequest, HttpResponse
from django.views.decorators.http import require_http_methods

from app.users.application.requests import CreateUserRequest
from app.users.domain.use_cases.create_user_use_case import CreateUserUseCase
from app.users.domain.exceptions import UserAlreadyExists
from app.users.domain.use_cases.get_all_users_use_case import GetAllUsersUseCase
from app.users.application.response import UserResponse


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
