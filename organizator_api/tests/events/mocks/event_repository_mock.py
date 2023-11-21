import uuid
from typing import List

from app.events.domain.exceptions import EventNotFound
from app.events.domain.models.event import Event
from app.events.domain.repositories import EventRepository


class EventRepositoryMock(EventRepository):
    def __init__(self) -> None:
        self.events: List[Event] = []

    def create(self, event: Event) -> None:
        self.events.append(event)

    def update(self, event: Event) -> None:
        pass

    def delete(self, event_id: uuid.UUID) -> None:
        pass

    def get(self, event_id: uuid.UUID) -> Event:
        for event in self.events:
            if event.id == event_id:
                return event
        raise EventNotFound

    def get_all(self) -> List[Event]:
        return self.events

    def clear(self) -> None:
        self.events = []