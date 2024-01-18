import uuid
from datetime import datetime, timezone

from app.answers.application.request import CreateAnswerRequest
from app.answers.domain.models.answer import Answer
from app.answers.infrastructure.repository_factories import AnswerRepositoryFactory
from app.applications.domain.usecases.get_application_use_case import (
    GetApplicationUseCase,
)
from app.questions.domain.usecases.get_question_by_id_use_case import (
    GetQuestionsByIdUseCase,
)


class CreateAnswerUseCase:
    def __init__(self) -> None:
        self.answer_repository = AnswerRepositoryFactory.create()

    def execute(self, answer_data: CreateAnswerRequest) -> None:
        application = GetApplicationUseCase().execute(
            application_id=answer_data.application_id
        )
        question = GetQuestionsByIdUseCase().execute(
            question_id=answer_data.question_id
        )

        answer = Answer(
            id=uuid.uuid4(),
            application=application,
            question=question,
            answer=answer_data.answer,
            created_at=datetime.now(tz=timezone.utc),
            updated_at=datetime.now(tz=timezone.utc),
        )

        self.answer_repository.create(answer)
