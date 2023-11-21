import uuid
from datetime import datetime, timezone

from app.events.application.requests import CreateEventRequest
from app.events.domain.models.event import Event
from app.events.infrastructure.repository_factories import EventRepositoryFactory


class CreateEventUseCase:
    def __init__(self) -> None:
        self.event_repository = EventRepositoryFactory.create()

    def execute(self, event_data: CreateEventRequest) -> None:
        event = Event(
            name=event_data.name,
            url=event_data.url,
            description=event_data.description,
            start_date=event_data.start_date,
            end_date=event_data.end_date,
            location=event_data.location,
            header_image=event_data.header_image,
            created_at=datetime.now(tz=timezone.utc),
            updated_at=datetime.now(tz=timezone.utc),
            id=uuid.uuid4(),
        )
        self.event_repository.create(event)
