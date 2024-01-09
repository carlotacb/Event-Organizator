import uuid
from typing import List

from app.applications.domain.models.application import Application
from app.applications.infrastructure.repository_factories import (
    ApplicationRepositoryFactory,
)
from app.users.domain.usecases.get_user_by_token_use_case import GetUserByTokenUseCase


class GetApplicationsByTokenUseCase:
    def __init__(self) -> None:
        self.application_repository = ApplicationRepositoryFactory.create()

    def execute(self, token: uuid.UUID) -> List[Application]:
        user = GetUserByTokenUseCase().execute(token=token)

        return self.application_repository.get_by_user(user=user)
