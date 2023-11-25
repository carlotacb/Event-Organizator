import uuid
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List

from app.events.domain.models.event import Event


class EventRepository(ABC):
    @abstractmethod
    def create(self, event: Event) -> None:
        pass

    @abstractmethod
    def update(self, event: Event) -> None:
        pass

    @abstractmethod
    def delete(self, event_id: uuid.UUID) -> None:
        pass

    @abstractmethod
    def get(self, event_id: uuid.UUID) -> Event:
        pass

    @abstractmethod
    def get_all(self) -> List[Event]:
        pass
