import uuid

from app.applications.domain.models.application import Application
from app.applications.infrastructure.repository_factories import (
    ApplicationRepositoryFactory,
)


class GetApplicationUseCase:
    def __init__(self) -> None:
        self.application_repository = ApplicationRepositoryFactory.create()

    def execute(self, application_id: uuid.UUID) -> Application:
        return self.application_repository.get(application_id)
