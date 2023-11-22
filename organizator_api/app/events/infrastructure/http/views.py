import json
from datetime import datetime

from django.http import HttpRequest, HttpResponse
from django.views.decorators.http import require_http_methods

from app.events.application.requests import CreateEventRequest
from app.events.domain.use_cases.create_event_use_case import CreateEventUseCase
from app.events.domain.exceptions import EventAlreadyExists


@require_http_methods(["POST"])
def create_new_event(request: HttpRequest) -> HttpResponse:
    json_body = json.loads(request.body)

    print(request)

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
        start_date=datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%SZ"),
        end_date=datetime.strptime(end_date, "%Y-%m-%dT%H:%M:%SZ"),
        location=location,
        header_image=header_image,
    )

    try:
        CreateEventUseCase().execute(event_data)
    except EventAlreadyExists:
        return HttpResponse(status=409, content="Event already exists")

    return HttpResponse(status=201, content="Event created correctly")