import json
import uuid

from django.http import HttpResponse, HttpRequest
from django.views.decorators.http import require_http_methods

from app.applications.domain.exceptions import ProfileNotComplete
from app.applications.domain.usecases.create_new_application_use_case import (
    CreateNewApplicationUseCase,
)
from app.events.domain.exceptions import EventNotFound
from app.users.domain.exceptions import UserNotFound


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
            event_id=event_id,
        )
    except ProfileNotComplete:
        return HttpResponse(status=422, content="Profile not complete")
    except UserNotFound:
        return HttpResponse(status=404, content="User not found")
    except EventNotFound:
        return HttpResponse(status=404, content="Event not found")

    return HttpResponse(status=201, content="Application created correctly")
