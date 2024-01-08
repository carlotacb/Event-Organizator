from typing import List

from app.applications.domain.exceptions import ApplicationAlreadyExists
from app.applications.domain.models.application import Application
from app.applications.domain.repositories import ApplicationRepository


class ApplicationRepositoryMock(ApplicationRepository):
    def __init__(self) -> None:
        self.applications: List[Application] = []

    def create(self, application: Application) -> None:
        for a in self.applications:
            if application.user.id == a.user.id and application.event.id == a.event.id:
                raise ApplicationAlreadyExists

        self.applications.append(application)

    def get_all(self) -> List[Application]:
        return self.applications

    def clear(self) -> None:
        self.applications = []
