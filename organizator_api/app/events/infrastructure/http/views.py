import json
import uuid
from datetime import datetime

from django.http import HttpRequest, HttpResponse
from django.views.decorators.http import require_http_methods

from app.events.application.requests import CreateEventRequest, UpdateEventRequest
from app.events.application.response import EventResponse
from app.events.domain.exceptions import EventAlreadyExists, EventNotFound
from app.events.domain.usecases.create_event_use_case import CreateEventUseCase
from app.events.domain.usecases.delete_event_use_case import DeleteEventUseCase
from app.events.domain.usecases.get_all_events_use_case import GetAllEventsUseCase
from app.events.domain.usecases.get_event_use_case import GetEventUseCase
from app.events.domain.usecases.update_event_use_case import UpdateEventUseCase


@require_http_methods(["POST"])
def create_new_event(request: HttpRequest) -> HttpResponse:
    json_body = json.loads(request.body)

    try:
        name = json_body["name"]
        url = json_body["url"]
        description = json_body["description"]
        start_date = json_body["start_date"]
        end_date = json_body["end_date"]
        location = json_body["location"]
        header_image = json_body["header_image"]
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
    )

    try:
        CreateEventUseCase().execute(event_data)
    except EventAlreadyExists:
        return HttpResponse(status=409, content="Event already exists")

    return HttpResponse(status=201, content="Event created correctly")


@require_http_methods(["GET"])
def get_all_events(request: HttpRequest) -> HttpResponse:
    all_events = GetAllEventsUseCase().execute()

    events_response = []
    for event in all_events:
        events_response.append(EventResponse.from_event(event).to_dict())

    return HttpResponse(
        status=200, content=json.dumps(events_response), content_type="application/json"
    )


@require_http_methods(["GET"])
def get_all_upcoming_events(request: HttpRequest) -> HttpResponse:
    all_events = GetAllEventsUseCase().execute()

    events_response = []
    for event in all_events:
        print(event.start_date)
        print(datetime.now())
        if event.deleted_at is None and event.start_date > datetime.now(tz=event.start_date.tzinfo):
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
    json_body = json.loads(request.body)

    name = json_body["name"] if "name" in json_body else None
    url = json_body["url"] if "url" in json_body else None
    description = json_body["description"] if "description" in json_body else None
    start_date = json_body["start_date"] if "start_date" in json_body else None
    end_date = json_body["end_date"] if "end_date" in json_body else None
    location = json_body["location"] if "location" in json_body else None
    header_image = json_body["header_image"] if "header_image" in json_body else None

    event_data = UpdateEventRequest(
        name=name,
        url=url,
        description=description,
        start_date=start_date
        if start_date
        else None,
        end_date=end_date
        if end_date
        else None,
        location=location,
        header_image=header_image,
    )

    try:
        event = UpdateEventUseCase().execute(event_id=event_id, event=event_data)
        event_response = EventResponse.from_event(event).to_dict()
    except EventAlreadyExists:
        return HttpResponse(status=409, content="Event already exists")
    except EventNotFound:
        return HttpResponse(status=404, content="Event does not exist")

    return HttpResponse(
        status=200, content=json.dumps(event_response), content_type="application/json"
    )


@require_http_methods(["POST"])
def delete_event(request: HttpRequest, event_id: uuid.UUID) -> HttpResponse:
    try:
        DeleteEventUseCase().execute(event_id=event_id)
    except EventNotFound:
        return HttpResponse(status=404, content="Event does not exist")

    return HttpResponse(status=200, content="Event updated correctly to be deleted")
