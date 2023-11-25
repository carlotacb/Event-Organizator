import uuid
from datetime import datetime, timezone
from typing import List

from django.db import IntegrityError

from app.events.domain.models.event import Event
from app.events.domain.repositories import EventRepository
from app.events.infrastructure.persistance.models.orm_event import ORMEvent
from app.events.domain.exceptions import EventAlreadyExists, EventNotFound


class ORMEventRepository(EventRepository):
    def create(self, event: Event) -> None:
        try:
            self._to_model(event).save()
        except IntegrityError:
            raise EventAlreadyExists()

    def update(self, event: Event) -> None:
        try:
            orm_event = ORMEvent.objects.get(id=event.id)
            orm_event.name = event.name
            orm_event.description = event.description
            orm_event.url = event.url
            orm_event.start_date = event.start_date
            orm_event.end_date = event.end_date
            orm_event.location = event.location
            orm_event.header_image = event.header_image
            orm_event.updated_at = event.updated_at
            orm_event.save()
        except ORMEvent.DoesNotExist:
            raise EventNotFound()
        except IntegrityError:
            raise EventAlreadyExists()

    def delete(self, event_id: uuid.UUID) -> None:
        pass  # pragma: no cover

    def get(self, event_id: uuid.UUID) -> Event:
        try:
            event = self._to_domain_model(ORMEvent.objects.get(id=event_id))
            return event
        except ORMEvent.DoesNotExist:
            raise EventNotFound()

    def get_all(self) -> List[Event]:
        return [self._to_domain_model(event) for event in ORMEvent.objects.all()]

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

    def _to_domain_model(self, event: ORMEvent) -> Event:
        return Event(
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
