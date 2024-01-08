from django.db import IntegrityError

from app.applications.domain.exceptions import ApplicationAlreadyExists
from app.applications.domain.models.application import Application
from app.applications.domain.repositories import ApplicationRepository
from app.applications.infrastructure.persistence.models.orm_application import (
    ORMEventApplication,
)
from app.events.infrastructure.persistence.models.orm_event import ORMEvent
from app.users.infrastructure.persistence.models.orm_user import ORMUser


class ORMApplicationRepository(ApplicationRepository):
    def create(self, application: Application) -> None:  # pragma: no cover
        user = ORMUser.objects.get(id=application.user.id)
        event = ORMEvent.objects.get(id=application.event.id)

        try:
            ORMEventApplication(
                id=application.id,
                user=user,
                event=event,
                created_at=application.created_at,
                updated_at=application.updated_at,
            ).save()
        except IntegrityError:
            raise ApplicationAlreadyExists
