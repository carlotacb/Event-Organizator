import uuid
from datetime import datetime, timezone

from app.events.domain.usecases.get_event_use_case import GetEventUseCase
from app.questions.application.request import CreateQuestionRequest
from app.questions.domain.models.question import Question, QuestionType
from app.questions.infrastructure.repository_factories import QuestionRepositoryFactory
from app.users.domain.exceptions import OnlyAuthorizedToOrganizerAdmin
from app.users.domain.models.user import UserRoles
from app.users.domain.usecases.get_role_by_token_use_case import GetRoleByTokenUseCase


class CreateNewQuestionUseCase:
    def __init__(self) -> None:
        self.question_repository = QuestionRepositoryFactory.create()

    def execute(self, question_data: CreateQuestionRequest, token: uuid.UUID) -> None:
        event = GetEventUseCase().execute(event_id=question_data.event_id)
        role = GetRoleByTokenUseCase().execute(token=token)

        if role != UserRoles.ORGANIZER_ADMIN:
            raise OnlyAuthorizedToOrganizerAdmin

        question = Question(
            id=uuid.uuid4(),
            event=event,
            question=question_data.question,
            question_type=QuestionType[question_data.question_type],
            options=question_data.options,
            created_at=datetime.now(tz=timezone.utc),
            updated_at=datetime.now(tz=timezone.utc),
        )

        self.question_repository.create(question)
