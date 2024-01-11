import json
import uuid

from django.http import HttpResponse, HttpRequest
from django.views.decorators.http import require_http_methods

from app.applications.application.response import ApplicationResponse
from app.applications.domain.exceptions import (
    ProfileNotComplete,
    ApplicationAlreadyExists,
    UserIsNotAParticipant,
    UserIsNotStudent,
    UserIsTooYoung,
    ApplicationNotFound, NotApplied,
)
from app.applications.domain.usecases.create_new_application_use_case import (
    CreateNewApplicationUseCase,
)
from app.applications.domain.usecases.get_application_status_by_event_use_case import (
    GetApplicationStatusByEventUseCase,
)
from app.applications.domain.usecases.get_applications_by_event_use_case import (
    GetApplicationsByEventUseCase,
)
from app.applications.domain.usecases.get_applications_by_token_use_case import (
    GetApplicationsByTokenUseCase,
)
from app.events.domain.exceptions import EventNotFound
from app.users.domain.exceptions import UserNotFound, OnlyAuthorizedToOrganizer


@require_http_methods(["POST"])
def create_new_application(request: HttpRequest) -> HttpResponse:
    token = request.headers.get("Authorization")
    if not token:
        return HttpResponse(status=401, content="Unauthorized")

    try:
        token_to_uuid = uuid.UUID(token)
    except ValueError:
        return HttpResponse(status=400, content="Invalid token")

    json_body = json.loads(request.body)

    if "event_id" not in json_body:
        return HttpResponse(status=422, content="Event id is required")

    event_id = json_body["event_id"]

    try:
        CreateNewApplicationUseCase().execute(
            token=token_to_uuid,
            event_id=uuid.UUID(event_id),
        )
    except UserNotFound:
        return HttpResponse(status=404, content="User not found")
    except ProfileNotComplete:
        return HttpResponse(status=422, content="Profile not complete")
    except EventNotFound:
        return HttpResponse(status=404, content="Event not found")
    except ApplicationAlreadyExists:
        return HttpResponse(status=409, content="Application already exists")
    except UserIsNotAParticipant:
        return HttpResponse(
            status=401, content="You should have role participant to apply"
        )
    except UserIsNotStudent:
        return HttpResponse(status=401, content="You should be student to apply")
    except UserIsTooYoung:
        return HttpResponse(status=401, content="You are too young to apply")

    return HttpResponse(status=201, content="Application created correctly")


@require_http_methods(["GET"])
def get_applications_by_token(request: HttpRequest) -> HttpResponse:
    token = request.headers.get("Authorization")
    if not token:
        return HttpResponse(status=401, content="Unauthorized")

    try:
        token_to_uuid = uuid.UUID(token)
    except ValueError:
        return HttpResponse(status=400, content="Invalid token")

    try:
        applications = GetApplicationsByTokenUseCase().execute(token=token_to_uuid)
    except UserNotFound:
        return HttpResponse(status=404, content="User not found")

    applications_response = []
    for application in applications:
        applications_response.append(
            ApplicationResponse.from_application(application).to_dict_without_user()
        )

    return HttpResponse(status=200, content=json.dumps(applications_response))


@require_http_methods(["GET"])
def get_applications_by_event(
    request: HttpRequest, event_id: uuid.UUID
) -> HttpResponse:
    token = request.headers.get("Authorization")
    if not token:
        return HttpResponse(status=401, content="Unauthorized")

    try:
        token_to_uuid = uuid.UUID(token)
    except ValueError:
        return HttpResponse(status=400, content="Invalid token")

    try:
        applications = GetApplicationsByEventUseCase().execute(
            token=token_to_uuid, event_id=event_id
        )
    except EventNotFound:
        return HttpResponse(status=404, content="Event not found")
    except OnlyAuthorizedToOrganizer:
        return HttpResponse(status=401, content="Only authorized to organizer")

    applications_response = []
    for application in applications:
        applications_response.append(
            ApplicationResponse.from_application(application).to_dict_without_event()
        )

    return HttpResponse(status=200, content=json.dumps(applications_response))


@require_http_methods(["GET"])
def get_application_status(request: HttpRequest, event_id: uuid.UUID) -> HttpResponse:
    token = request.headers.get("Authorization")
    if not token:
        return HttpResponse(status=401, content="Unauthorized")

    try:
        token_to_uuid = uuid.UUID(token)
    except ValueError:
        return HttpResponse(status=400, content="Invalid token")

    try:
        status = GetApplicationStatusByEventUseCase().execute(
            token=token_to_uuid, event_id=event_id
        )
    except NotApplied:
        return HttpResponse(status=206, content="Not applied")
    except UserIsNotAParticipant:
        return HttpResponse(status=401, content="You are not a participant")
    except EventNotFound:
        return HttpResponse(status=404, content="Event not found")
    except UserNotFound:
        return HttpResponse(status=404, content="User not found")

    return HttpResponse(status=200, content=json.dumps({"status": status.value}))
