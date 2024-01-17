import uuid
from datetime import datetime, timezone

from app.questions.application.request import UpdateQuestionRequest
from app.questions.domain.models.question import QuestionType
from app.questions.infrastructure.repository_factories import QuestionRepositoryFactory
from app.users.domain.exceptions import OnlyAuthorizedToOrganizerAdmin
from app.users.domain.models.user import UserRoles
from app.users.domain.usecases.get_role_by_token_use_case import GetRoleByTokenUseCase


class UpdateQuestionUseCase:
    def __init__(self) -> None:
        self.question_repository = QuestionRepositoryFactory.create()

    def execute(
        self,
        question_id: uuid.UUID,
        question_data: UpdateQuestionRequest,
        token: uuid.UUID,
    ) -> None:
        role = GetRoleByTokenUseCase().execute(token=token)

        if role != UserRoles.ORGANIZER_ADMIN:
            raise OnlyAuthorizedToOrganizerAdmin

        question = self.question_repository.get(question_id)
        question.question = question_data.question
        question.question_type = QuestionType[question_data.question_type]
        question.options = question_data.options
        question.updated_at = datetime.now(tz=timezone.utc)

        self.question_repository.update(question)
