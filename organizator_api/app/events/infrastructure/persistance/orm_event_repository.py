import uuid
from typing import List

from app.events.domain.models.event import Event
from app.events.domain.repositories import EventRepository
from app.events.infrastructure.persistance.models.orm_event import ORMEvent


class ORMEventRepository(EventRepository):
    def create(self, event: Event) -> None:
        pass  # pragma: no cover

    def update(self, event: Event) -> None:
        pass  # pragma: no cover

    def delete(self, event_id: uuid.UUID) -> None:
        pass  # pragma: no cover

    def get(self, event_id: uuid.UUID) -> Event:  # type: ignore
        pass  # pragma: no cover

    def get_all(self) -> List[Event]:  # type: ignore
        pass  # pragma: no cover

    def to_model(self, event: Event) -> ORMEvent:  # type: ignore
        pass  # pragma: no cover
