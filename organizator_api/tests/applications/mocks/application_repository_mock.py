import uuid
from typing import List

from app.applications.domain.exceptions import (
    ApplicationAlreadyExists,
    ApplicationNotFound,
)
from app.applications.domain.models.application import Application
from app.applications.domain.repositories import ApplicationRepository
from app.users.domain.models.user import User


class ApplicationRepositoryMock(ApplicationRepository):
    def __init__(self) -> None:
        self.applications: List[Application] = []

    def create(self, application: Application) -> None:
        for a in self.applications:
            if application.user.id == a.user.id and application.event.id == a.event.id:
                raise ApplicationAlreadyExists

        self.applications.append(application)

    def get_by_user(self, user: User) -> List[Application]:
        applications = []
        for a in self.applications:
            if user.id == a.user.id:
                applications.append(a)

        return applications

    def get_by_event(self, event_id: uuid.UUID) -> List[Application]:
        applications = []
        for a in self.applications:
            if event_id == a.event.id:
                applications.append(a)

        return applications

    def get_application(self, event_id: uuid.UUID, user_id: uuid.UUID) -> Application:
        for a in self.applications:
            if event_id == a.event.id and user_id == a.user.id:
                return a

        raise ApplicationNotFound

    def get_all(self) -> List[Application]:
        return self.applications

    def clear(self) -> None:
        self.applications = []
