from abc import ABC, abstractmethod

from app.applications.domain.models.application import Application


class ApplicationRepository(ABC):
    @abstractmethod
    def create(self, application: Application) -> None:
        pass
