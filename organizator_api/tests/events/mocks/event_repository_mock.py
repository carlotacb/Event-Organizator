import uuid
from typing import List

from app.events.domain.exceptions import EventNotFound, EventAlreadyExists
from app.events.domain.models.event import Event
from app.events.domain.repositories import EventRepository


class EventRepositoryMock(EventRepository):
    def __init__(self) -> None:
        self.events: List[Event] = []

    def create(self, event: Event) -> None:
        for e in self.events:
            if event.name == e.name:
                raise EventAlreadyExists

        self.events.append(event)

    def update(self, event: Event) -> None:
        for e in self.events:
            if e.name == event.name and e.id != event.id:
                raise EventAlreadyExists
            if e.id == event.id:
                return

        raise EventNotFound

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
