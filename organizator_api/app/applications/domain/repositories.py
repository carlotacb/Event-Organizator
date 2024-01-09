import uuid
from abc import ABC, abstractmethod
from typing import List

from app.applications.domain.models.application import Application
from app.events.domain.models.event import Event
from app.users.domain.models.user import User


class ApplicationRepository(ABC):
    @abstractmethod
    def create(self, application: Application) -> None:
        pass

    @abstractmethod
    def get_by_user(self, user: User) -> List[Application]:
        pass

    @abstractmethod
    def get_by_event(self, event_id: uuid.UUID) -> List[Application]:
        pass
