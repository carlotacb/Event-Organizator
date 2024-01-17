import uuid
from typing import List

from app.questions.domain.models.question import Question
from app.questions.infrastructure.repository_factories import QuestionRepositoryFactory
from app.users.domain.usecases.get_role_by_token_use_case import GetRoleByTokenUseCase


class GetQuestionsByEventUseCase:
    def __init__(self) -> None:
        self.question_repository = QuestionRepositoryFactory.create()

    def execute(self, event_id: uuid.UUID, token: uuid.UUID) -> List[Question]:
        GetRoleByTokenUseCase().execute(token=token)

        return self.question_repository.get_by_event_id(event_id)
