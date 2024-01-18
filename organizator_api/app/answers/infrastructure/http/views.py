import json
import uuid

from django.http import HttpResponse, HttpRequest
from django.views.decorators.http import require_http_methods

from app.answers.application.request import CreateAnswerRequest
from app.answers.application.responses import AnswerResponse
from app.answers.domain.exceptions import UserIsNotAuthorOfAnswer
from app.answers.domain.usecases.create_answer_use_case import CreateAnswerUseCase
from app.answers.domain.usecases.get_answers_by_application_id_use_case import (
    GetAnswersByApplicationIdUseCase,
)
from app.applications.domain.exceptions import ApplicationNotFound
from app.questions.domain.exceptions import QuestionDoesNotExist


@require_http_methods(["POST"])
def create_new_answer(request: HttpRequest) -> HttpResponse:
    token = request.headers.get("Authorization")
    if not token:
        return HttpResponse(status=401, content="Unauthorized")

    try:
        uuid.UUID(token)
    except ValueError:
        return HttpResponse(status=400, content="Invalid token")

    json_body = json.loads(request.body)

    try:
        application_id = json_body["application_id"]
        question_id = json_body["question_id"]
        answer = json_body["answer"]
    except (TypeError, KeyError):
        return HttpResponse(status=400, content="Unexpected body")

    answer_data = CreateAnswerRequest(
        application_id=uuid.UUID(application_id),
        question_id=uuid.UUID(question_id),
        answer=answer,
    )

    try:
        CreateAnswerUseCase().execute(answer_data)
    except ApplicationNotFound:
        return HttpResponse(status=404, content="Application not found")
    except QuestionDoesNotExist:
        return HttpResponse(status=404, content="Question not found")

    return HttpResponse(status=201, content="Answer created correctly")


@require_http_methods(["GET"])
def get_answers_for_application(
    request: HttpRequest, application_id: uuid.UUID
) -> HttpResponse:
    token = request.headers.get("Authorization")
    if not token:
        return HttpResponse(status=401, content="Unauthorized")

    try:
        token_for_uuid = uuid.UUID(token)
    except ValueError:
        return HttpResponse(status=400, content="Invalid token")

    try:
        answers = GetAnswersByApplicationIdUseCase().execute(
            application_id=application_id, token=token_for_uuid
        )
    except ApplicationNotFound:
        return HttpResponse(status=404, content="Application not found")
    except UserIsNotAuthorOfAnswer:
        return HttpResponse(status=401, content="User is not author of answer")

    answers_response = []
    for answer in answers:
        answers_response.append(AnswerResponse.from_answer(answer).to_dict())

    return HttpResponse(status=200, content=json.dumps(answers_response))
