import json
import uuid

from django.http import HttpRequest, HttpResponse
from django.views.decorators.http import require_http_methods

from app.events.domain.exceptions import MissingWorkInformationToCreateUser, MissingStudyInformationToCreateUser
from app.users.application.requests import CreateUserRequest, UpdateUserRequest
from app.users.application.response import UserResponse
from app.users.domain.exceptions import (
    UserAlreadyExists,
    UserNotFound,
    InvalidPassword,
    OnlyAuthorizedToOrganizerAdmin,
)
from app.users.domain.usecases.create_user_use_case import CreateUserUseCase
from app.users.domain.usecases.get_all_users_use_case import GetAllUsersUseCase
from app.users.domain.usecases.get_role_by_token_use_case import GetRoleByTokenUseCase
from app.users.domain.usecases.get_user_by_id_use_case import GetUserByIdUseCase
from app.users.domain.usecases.get_user_by_token_use_case import GetUserByTokenUseCase
from app.users.domain.usecases.get_user_by_username_use_case import (
    GetUserByUsernameUseCase,
)
from app.users.domain.usecases.login_use_case import LoginUseCase
from app.users.domain.usecases.logout_use_case import LogoutUseCase
from app.users.domain.usecases.update_user_role_use_case import UpdateUserRoleUseCase
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
        date_of_birth = json_body["date_of_birth"]
        study = json_body["study"] if "study" in json_body else False
        work = json_body["work"] if "work" in json_body else False
        university = json_body["university"] if "university" in json_body else None
        degree = json_body["degree"] if "degree" in json_body else None
        expected_graduation = json_body["expected_graduation"] if "expected_graduation" in json_body else None
        current_job_role = json_body["current_job_role"] if "current_job_role" in json_body else None
    except (TypeError, KeyError):
        return HttpResponse(status=422, content="Unexpected body")

    user_data = CreateUserRequest(
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
        username=username,
        bio=bio,
        profile_image=profile_image,
        date_of_birth=date_of_birth,
        study=study,
        work=work,
        university=university,
        degree=degree,
        expected_graduation=expected_graduation,
        current_job_role=current_job_role,
    )

    try:
        CreateUserUseCase().execute(user_data)
    except MissingWorkInformationToCreateUser:
        return HttpResponse(status=422, content="Missing work information to create user")
    except MissingStudyInformationToCreateUser:
        return HttpResponse(status=422, content="Missing study information to create user")
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


@require_http_methods(["GET"])
def get_user_by_token(request: HttpRequest) -> HttpResponse:
    token = request.headers.get("Authorization")

    if not token:
        return HttpResponse(status=401, content="Unauthorized")

    try:
        token_to_uuid = uuid.UUID(token)
    except ValueError:
        return HttpResponse(status=400, content="Invalid token")

    try:
        user = GetUserByTokenUseCase().execute(token=token_to_uuid)
    except UserNotFound:
        return HttpResponse(status=404, content="User does not exist")

    return HttpResponse(
        status=200,
        content=json.dumps(UserResponse.from_user(user).to_dict()),
        content_type="application/json",
    )


@require_http_methods(["GET"])
def get_role_by_token(request: HttpRequest) -> HttpResponse:
    token = request.headers.get("Authorization")

    if not token:
        return HttpResponse(status=401, content="Unauthorized")

    try:
        token_to_uuid = uuid.UUID(token)
    except ValueError:
        return HttpResponse(status=400, content="Invalid token")

    try:
        role = GetRoleByTokenUseCase().execute(token=token_to_uuid)
    except UserNotFound:
        return HttpResponse(status=404, content="User does not exist")

    return HttpResponse(
        status=200,
        content=json.dumps({"role": role.value}),
        content_type="application/json",
    )


@require_http_methods(["POST"])
def update_my_user(request: HttpRequest) -> HttpResponse:
    token = request.headers.get("Authorization")
    if not token:
        return HttpResponse(status=401, content="Unauthorized")

    try:
        token_to_uuid = uuid.UUID(token)
    except ValueError:
        return HttpResponse(status=400, content="Invalid token")

    json_body = json.loads(request.body)

    if "email" in json_body:
        return HttpResponse(status=403, content="The email cannot be updated")
    if "password" in json_body:
        return HttpResponse(status=403, content="The password cannot be updated")

    first_name = json_body["first_name"] if "first_name" in json_body else None
    last_name = json_body["last_name"] if "last_name" in json_body else None
    username = json_body["username"] if "username" in json_body else None
    bio = json_body["bio"] if "bio" in json_body else None
    profile_image = json_body["profile_image"] if "profile_image" in json_body else None
    date_of_birth = json_body["date_of_birth"] if "date_of_birth" in json_body else None
    study = json_body["study"] if "study" in json_body else None
    work = json_body["work"] if "work" in json_body else None
    university = json_body["university"] if "university" in json_body else None
    degree = json_body["degree"] if "degree" in json_body else None
    expected_graduation = json_body["expected_graduation"] if "expected_graduation" in json_body else None
    current_job_role = json_body["current_job_role"] if "current_job_role" in json_body else None
    tshirt = json_body["tshirt"] if "tshirt" in json_body else None
    gender = json_body["gender"] if "gender" in json_body else None
    alimentary_restrictions = json_body["alimentary_restrictions"] if "alimentary_restrictions" in json_body else None
    github = json_body["github"] if "github" in json_body else None
    linkedin = json_body["linkedin"] if "linkedin" in json_body else None
    devpost = json_body["devpost"] if "devpost" in json_body else None
    webpage = json_body["webpage"] if "webpage" in json_body else None


    user_data = UpdateUserRequest(
        username=username,
        first_name=first_name,
        last_name=last_name,
        bio=bio,
        profile_image=profile_image,
        date_of_birth=date_of_birth,
        study=study,
        work=work,
        university=university,
        degree=degree,
        expected_graduation=expected_graduation,
        current_job_role=current_job_role,
        tshirt=tshirt,
        gender=gender,
        alimentary_restrictions=alimentary_restrictions,
        github=github,
        linkedin=linkedin,
        devpost=devpost,
        webpage=webpage,
    )

    try:
        user = UpdateUserUseCase().execute(token=token_to_uuid, user_data=user_data)
    except MissingWorkInformationToCreateUser:
        return HttpResponse(status=422, content="Missing work information to create user")
    except MissingStudyInformationToCreateUser:
        return HttpResponse(status=422, content="Missing study information to create user")
    except UserNotFound:
        return HttpResponse(status=404, content="User does not exist")
    except UserAlreadyExists:
        return HttpResponse(status=409, content="The username you are using is already taken")

    return HttpResponse(
        status=200,
        content=json.dumps(UserResponse.from_user(user).to_dict()),
        content_type="application/json",
    )


@require_http_methods(["POST"])
def update_role(request: HttpRequest, user_id: uuid.UUID) -> HttpResponse:
    token = request.headers.get("Authorization")
    if not token:
        return HttpResponse(status=401, content="Unauthorized")

    try:
        token_to_uuid = uuid.UUID(token)
    except ValueError:
        return HttpResponse(status=400, content="Invalid token")

    json_body = json.loads(request.body)

    try:
        role = json_body["role"]
    except (TypeError, KeyError):
        return HttpResponse(status=422, content="Unexpected body")

    try:
        user = UpdateUserRoleUseCase().execute(
            user_id=user_id, new_role=role, token=token_to_uuid
        )
    except UserNotFound:
        return HttpResponse(status=404, content="User does not exist")
    except OnlyAuthorizedToOrganizerAdmin:
        return HttpResponse(status=401, content="Only authorized to organizer admin")
    except (ValueError, KeyError):
        return HttpResponse(status=400, content="Invalid role")

    return HttpResponse(
        status=200,
        content=json.dumps(UserResponse.from_user(user).to_dict()),
        content_type="application/json",
    )


@require_http_methods(["POST"])
def login(request: HttpRequest) -> HttpResponse:
    json_body = json.loads(request.body)

    if "username" not in json_body:
        return HttpResponse(status=422, content="Username is required")
    if "password" not in json_body:
        return HttpResponse(status=422, content="Password is required")

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


@require_http_methods(["POST"])
def logout(request: HttpRequest) -> HttpResponse:
    token = request.headers.get("Authorization")
    if not token:
        return HttpResponse(status=401, content="Unauthorized")

    try:
        token_to_uuid = uuid.UUID(token)
    except ValueError:
        return HttpResponse(status=400, content="Invalid token")

    LogoutUseCase().execute(token=token_to_uuid)

    return HttpResponse(status=200, content="User logged out correctly")
