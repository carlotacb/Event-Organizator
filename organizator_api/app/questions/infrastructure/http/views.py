import json
import uuid

from django.http import HttpResponse, HttpRequest
from django.views.decorators.http import require_http_methods

from app.events.domain.exceptions import EventNotFound
from app.questions.application.request import CreateQuestionRequest, UpdateQuestionRequest
from app.questions.domain.exceptions import QuestionDoesNotExist
from app.questions.domain.usecases.create_new_question_use_case import (
    CreateNewQuestionUseCase,
)
from app.questions.domain.usecases.update_question_use_case import UpdateQuestionUseCase
from app.users.domain.exceptions import OnlyAuthorizedToOrganizerAdmin


@require_http_methods(["POST"])
def create_new_question(request: HttpRequest) -> HttpResponse:
    token = request.headers.get("Authorization")
    if not token:
        return HttpResponse(status=401, content="Unauthorized")

    try:
        token_to_uuid = uuid.UUID(token)
    except ValueError:
        return HttpResponse(status=400, content="Invalid token")

    json_body = json.loads(request.body)

    try:
        event_id = uuid.UUID(json_body["event_id"])
    except ValueError:
        return HttpResponse(status=400, content="Invalid event id")

    try:
        question = json_body["question"]
        question_type = json_body["question_type"]
        options = json_body["options"] if "options" in json_body else ""
    except KeyError:
        return HttpResponse(status=400, content="Unexpected body")

    question_data = CreateQuestionRequest(
        question=question,
        question_type=question_type,
        options=options,
        event_id=event_id,
    )

    try:
        CreateNewQuestionUseCase().execute(
            question_data=question_data, token=token_to_uuid
        )
    except EventNotFound:
        return HttpResponse(status=404, content="Event does not exist")
    except OnlyAuthorizedToOrganizerAdmin:
        return HttpResponse(
            status=401, content="Only organizer admins can create questions"
        )

    return HttpResponse(status=201, content="Question created correctly")

@require_http_methods(["POST"])
def update_question(request: HttpRequest, question_id: uuid.UUID) -> HttpResponse:
    token = request.headers.get("Authorization")
    if not token:
        return HttpResponse(status=401, content="Unauthorized")

    try:
        token_to_uuid = uuid.UUID(token)
    except ValueError:
        return HttpResponse(status=400, content="Invalid token")

    json_body = json.loads(request.body)

    question = json_body["question"] if "question" in json_body else None
    question_type = json_body["question_type"] if "question_type" in json_body else None
    options = json_body["options"] if "options" in json_body else None

    try:
        UpdateQuestionUseCase().execute(
            question_id=question_id,
            question_data=UpdateQuestionRequest(
                question=question,
                question_type=question_type,
                options=options
            ),
            token=token_to_uuid
        )
    except OnlyAuthorizedToOrganizerAdmin:
        return HttpResponse(
            status=401, content="Only organizer admins can update questions"
        )
    except QuestionDoesNotExist:
        return HttpResponse(status=404, content="Question does not exist")

    return HttpResponse(status=200, content="Question updated correctly")
