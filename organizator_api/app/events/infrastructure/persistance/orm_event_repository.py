import uuid
from typing import List

from app.events.domain.models.event import Event
from app.events.domain.repositories import EventRepository
from app.events.infrastructure.persistance.models.orm_event import ORMEvent


class ORMEventRepository(EventRepository):
    def create(self, event: Event) -> None:
        pass

    def update(self, event: Event) -> None:
        pass

    def delete(self, event_id: uuid.UUID) -> None:
        pass

    def get(self, event_id: uuid.UUID) -> Event:  # type: ignore
        pass

    def get_all(self) -> List[Event]:  # type: ignore
        pass

    def to_model(self, event: Event) -> ORMEvent:  # type: ignore
        pass
