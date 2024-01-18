import json
import uuid

from django.http import HttpResponse, HttpRequest
from django.views.decorators.http import require_http_methods

from app.answers.application.request import CreateAnswerRequest
from app.answers.domain.exceptions import AnswerAlreadyExists
from app.answers.domain.usecases.create_answer_use_case import CreateAnswerUseCase
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
