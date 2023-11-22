import uuid
from typing import List

from django.db import IntegrityError

from app.events.domain.models.event import Event
from app.events.domain.repositories import EventRepository
from app.events.infrastructure.persistance.models.orm_event import ORMEvent
from app.events.domain.exceptions import EventAlreadyExists


class ORMEventRepository(EventRepository):
    def create(self, event: Event) -> None:
        try:
            self._to_model(event).save()
        except Exception as e:
            raise EventAlreadyExists()

    def update(self, event: Event) -> None:
        pass  # pragma: no cover

    def delete(self, event_id: uuid.UUID) -> None:
        pass  # pragma: no cover

    def get(self, event_id: uuid.UUID) -> Event:  # type: ignore
        pass  # pragma: no cover

    def get_all(self) -> List[Event]:  # type: ignore
        pass  # pragma: no cover

    def _to_model(self, event: Event) -> ORMEvent:
        return ORMEvent(
            id=event.id,
            name=event.name,
            description=event.description,
            url=event.url,
            start_date=event.start_date,
            end_date=event.end_date,
            location=event.location,
            header_image=event.header_image,
            created_at=event.created_at,
            updated_at=event.updated_at,
            deleted_at=event.deleted_at,
        )
