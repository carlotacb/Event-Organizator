import uuid
from typing import List

from app.answers.domain.exceptions import UserIsNotAuthorOfAnswer
from app.answers.domain.models.answer import Answer
from app.answers.infrastructure.repository_factories import AnswerRepositoryFactory
from app.applications.domain.usecases.get_application_use_case import (
    GetApplicationUseCase,
)
from app.users.domain.usecases.get_user_by_token_use_case import GetUserByTokenUseCase


class GetAnswersByApplicationIdUseCase:
    def __init__(self) -> None:
        self.answer_repository = AnswerRepositoryFactory.create()

    def execute(self, application_id: uuid.UUID, token: uuid.UUID) -> List[Answer]:
        user = GetUserByTokenUseCase().execute(token=token)
        application = GetApplicationUseCase().execute(application_id=application_id)

        if user.id != application.user.id:
            raise UserIsNotAuthorOfAnswer

        return self.answer_repository.get_by_application_id(application_id)
