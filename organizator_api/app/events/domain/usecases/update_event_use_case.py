import uuid
from datetime import timezone, datetime

from app.events.application.requests import UpdateEventRequest
from app.events.domain.models.event import Event
from app.events.infrastructure.repository_factories import EventRepositoryFactory


class UpdateEventUseCase:
    def __init__(self) -> None:
        self.event_repository = EventRepositoryFactory.create()

    def execute(self, event_id: uuid.UUID, event: UpdateEventRequest) -> Event:
        original_event = self.event_repository.get(event_id)
        new_event = Event(
            id=event_id,
            name=event.name if event.name else original_event.name,
            description=event.description
            if event.description
            else original_event.description,
            url=event.url if event.url else original_event.url,
            start_date=datetime.strptime(event.start_date, "%d/%m/%Y %H:%M")
            if event.start_date
            else original_event.start_date,
            end_date=datetime.strptime(event.end_date, "%d/%m/%Y %H:%M") if event.end_date else original_event.end_date,
            location=event.location if event.location else original_event.location,
            header_image=event.header_image
            if event.header_image
            else original_event.header_image,
            created_at=original_event.created_at,
            updated_at=datetime.now(tz=timezone.utc),
        )

        self.event_repository.update(new_event)

        return new_event
