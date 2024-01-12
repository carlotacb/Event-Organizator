import uuid
from abc import ABC, abstractmethod
from typing import List

from app.applications.domain.models.application import Application
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

    @abstractmethod
    def get_application(self, event_id: uuid.UUID, user_id: uuid.UUID) -> Application:
        pass

    @abstractmethod
    def update(self, application: Application) -> None:
        pass

    @abstractmethod
    def get(self, application_id: uuid.UUID) -> Application:
        pass
