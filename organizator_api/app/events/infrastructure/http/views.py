import json
import uuid
from datetime import datetime

from django.http import HttpRequest, HttpResponse
from django.views.decorators.http import require_http_methods

from app.events.application.requests import CreateEventRequest, UpdateEventRequest
from app.events.application.response import EventResponse, EventApplicationResponse
from app.events.domain.exceptions import EventAlreadyExists, EventNotFound
from app.events.domain.usecases.create_event_use_case import CreateEventUseCase
from app.events.domain.usecases.delete_event_use_case import DeleteEventUseCase
from app.events.domain.usecases.get_all_events_use_case import GetAllEventsUseCase
from app.events.domain.usecases.get_event_use_case import GetEventUseCase
from app.events.domain.usecases.get_upcoming_events_and_participants_use_case import (
    GetUpcomingEventsAndParticipantsUseCase,
)
from app.events.domain.usecases.update_event_use_case import UpdateEventUseCase
from app.users.domain.exceptions import (
    OnlyAuthorizedToOrganizerAdmin,
    OnlyAuthorizedToOrganizer,
    UserNotFound,
)


@require_http_methods(["POST"])
def create_new_event(request: HttpRequest) -> HttpResponse:
    token = request.headers.get("Authorization")
    if not token:
        return HttpResponse(status=401, content="Unauthorized")

    try:
        token_to_uuid = uuid.UUID(token)
    except ValueError:
        return HttpResponse(status=400, content="Invalid token")

    json_body = json.loads(request.body)

    try:
        name = json_body["name"]
        url = json_body["url"]
        description = json_body["description"]
        start_date = json_body["start_date"]
        end_date = json_body["end_date"]
        location = json_body["location"]
        header_image = json_body["header_image"]
        open_for_participants = json_body["open_for_participants"]
        max_participants = json_body["max_participants"]
        expected_attrition_rate = json_body["expected_attrition_rate"]
        students_only = json_body["students_only"]
        age_restrictions = json_body["age_restrictions"]
    except (TypeError, KeyError):
        return HttpResponse(status=400, content="Unexpected body")

    event_data = CreateEventRequest(
        name=name,
        url=url,
        description=description,
        start_date=start_date,
        end_date=end_date,
        location=location,
        header_image=header_image,
        open_for_participants=open_for_participants,
        max_participants=max_participants,
        expected_attrition_rate=expected_attrition_rate,
        students_only=students_only,
        age_restrictions=age_restrictions,
    )

    try:
        CreateEventUseCase().execute(token_to_uuid, event_data)
    except EventAlreadyExists:
        return HttpResponse(status=409, content="Event already exists")
    except OnlyAuthorizedToOrganizerAdmin:
        return HttpResponse(
            status=401, content="Only organizer admins can create events"
        )

    return HttpResponse(status=201, content="Event created correctly")


@require_http_methods(["GET"])
def get_all_events(request: HttpRequest) -> HttpResponse:
    all_events = GetAllEventsUseCase().execute()

    events_response = []
    for event in all_events:
        if event.deleted_at is None:
            events_response.append(EventResponse.from_event(event).to_dict())

    return HttpResponse(
        status=200, content=json.dumps(events_response), content_type="application/json"
    )


@require_http_methods(["GET"])
def get_all_upcoming_events(request: HttpRequest) -> HttpResponse:
    all_events = GetAllEventsUseCase().execute()

    events_response = []
    for event in all_events:
        if event.deleted_at is None and event.start_date > datetime.now(
            tz=event.start_date.tzinfo
        ):
            events_response.append(EventResponse.from_event(event).to_dict())

    return HttpResponse(
        status=200, content=json.dumps(events_response), content_type="application/json"
    )


@require_http_methods(["GET"])
def get_event(request: HttpRequest, event_id: uuid.UUID) -> HttpResponse:
    try:
        event = GetEventUseCase().execute(event_id=event_id)
    except EventNotFound:
        return HttpResponse(status=404, content="Event does not exist")

    event_response = EventResponse.from_event(event).to_dict()

    return HttpResponse(
        status=200, content=json.dumps(event_response), content_type="application/json"
    )


@require_http_methods(["POST"])
def update_event(request: HttpRequest, event_id: uuid.UUID) -> HttpResponse:
    token = request.headers.get("Authorization")
    if not token:
        return HttpResponse(status=401, content="Unauthorized")

    try:
        token_to_uuid = uuid.UUID(token)
    except ValueError:
        return HttpResponse(status=400, content="Invalid token")

    json_body = json.loads(request.body)

    name = json_body["name"] if "name" in json_body else None
    url = json_body["url"] if "url" in json_body else None
    description = json_body["description"] if "description" in json_body else None
    start_date = json_body["start_date"] if "start_date" in json_body else None
    end_date = json_body["end_date"] if "end_date" in json_body else None
    location = json_body["location"] if "location" in json_body else None
    header_image = json_body["header_image"] if "header_image" in json_body else None
    open_for_participants = (
        json_body["open_for_participants"]
        if "open_for_participants" in json_body
        else None
    )
    max_participants = (
        json_body["max_participants"] if "max_participants" in json_body else None
    )
    expected_attrition_rate = (
        json_body["expected_attrition_rate"]
        if "expected_attrition_rate" in json_body
        else None
    )
    students_only = json_body["students_only"] if "students_only" in json_body else None
    age_restrictions = (
        json_body["age_restrictions"] if "age_restrictions" in json_body else None
    )

    event_data = UpdateEventRequest(
        name=name,
        url=url,
        description=description,
        start_date=start_date if start_date else None,
        end_date=end_date if end_date else None,
        location=location,
        header_image=header_image,
        open_for_participants=open_for_participants,
        max_participants=max_participants,
        expected_attrition_rate=expected_attrition_rate,
        students_only=students_only,
        age_restrictions=age_restrictions,
    )

    try:
        event = UpdateEventUseCase().execute(
            token=token_to_uuid, event_id=event_id, event=event_data
        )
        event_response = EventResponse.from_event(event).to_dict()
    except EventAlreadyExists:
        return HttpResponse(status=409, content="Event already exists")
    except EventNotFound:
        return HttpResponse(status=404, content="Event does not exist")
    except OnlyAuthorizedToOrganizer:
        return HttpResponse(status=401, content="Only organizers can update events")

    return HttpResponse(
        status=200, content=json.dumps(event_response), content_type="application/json"
    )


@require_http_methods(["POST"])
def delete_event(request: HttpRequest, event_id: uuid.UUID) -> HttpResponse:
    token = request.headers.get("Authorization")
    if not token:
        return HttpResponse(status=401, content="Unauthorized")

    try:
        token_to_uuid = uuid.UUID(token)
    except ValueError:
        return HttpResponse(status=400, content="Invalid token")

    try:
        DeleteEventUseCase().execute(token=token_to_uuid, event_id=event_id)
    except EventNotFound:
        return HttpResponse(status=404, content="Event does not exist")
    except OnlyAuthorizedToOrganizerAdmin:
        return HttpResponse(
            status=401, content="Only organizer admins can delete events"
        )

    return HttpResponse(status=200, content="Event updated correctly to be deleted")


@require_http_methods(["GET"])
def get_upcoming_events_with_application_information(
    request: HttpRequest,
) -> HttpResponse:
    token = request.headers.get("Authorization")
    if not token:
        return HttpResponse(status=401, content="Unauthorized")

    try:
        token_to_uuid = uuid.UUID(token)
    except ValueError:
        return HttpResponse(status=400, content="Invalid token")

    try:
        upcoming_events = GetUpcomingEventsAndParticipantsUseCase().execute(
            token=token_to_uuid
        )
    except UserNotFound:
        return HttpResponse(status=404, content="User does not exist")
    except OnlyAuthorizedToOrganizer:
        return HttpResponse(
            status=401, content="Only organizers can get this information"
        )

    events_response = []
    for event in upcoming_events:
        events_response.append(
            EventApplicationResponse.from_event_application(event).to_dict()
        )

    return HttpResponse(
        status=200, content=json.dumps(events_response), content_type="application/json"
    )
