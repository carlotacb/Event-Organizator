import json

from django.http import HttpRequest, HttpResponse
from django.views.decorators.http import require_http_methods

from app.users.application.requests import CreateUserRequest
from app.users.domain.use_cases.create_user_use_case import CreateUserUseCase
from app.users.domain.exceptions import UserAlreadyExists


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
