import uuid
from typing import List

from app.applications.domain.models.application import Application
from app.applications.infrastructure.repository_factories import ApplicationRepositoryFactory


class GetApplicationsByEventUseCase:
    def __init__(self) -> None:
        self.application_repository = ApplicationRepositoryFactory.create()

    def execute(self, event_id: uuid.UUID) -> List[Application]:
        return self.application_repository.get_by_event(event_id=event_id)