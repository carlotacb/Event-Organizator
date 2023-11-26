from datetime import datetime, timezone
import uuid

from app.events.infrastructure.repository_factories import EventRepositoryFactory


class DeleteEventUseCase:
    def __init__(self) -> None:
        self.event_repository = EventRepositoryFactory.create()

    def execute(self, event_id: uuid.UUID) -> None:
        self.event_repository.delete(event_id, datetime.now(timezone.utc))
