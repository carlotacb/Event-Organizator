import uuid

from app.events.infrastructure.repository_factories import EventRepositoryFactory
from app.events.domain.models.event import Event


class GetEventUseCase:
    def __init__(self) -> None:
        self.event_repository = EventRepositoryFactory.create()

    def execute(self, event_id: uuid.UUID) -> Event:
        return self.event_repository.get(event_id)