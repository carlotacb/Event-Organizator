from django.db import IntegrityError

from app.applications.domain.exceptions import ApplicationAlreadyExists
from app.applications.domain.models.application import Application
from app.applications.domain.repositories import ApplicationRepository
from app.applications.infrastructure.persistence.models.orm_application import ORMApplication


class ORMApplicationRepository(ApplicationRepository):

    def create(self, application: Application) -> None:
        try:
            self._to_model(application).save()
        except IntegrityError:
            raise ApplicationAlreadyExists

    def _to_model(self, application: Application) -> ORMApplication:
        return ORMApplication(
            id=application.id,
            user_id=application.user_id,
            event_id=application.event_id,
            created_at=application.created_at,
            updated_at=application.updated_at,
        )