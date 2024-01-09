import uuid
from typing import List

from django.db import IntegrityError

from app.applications.domain.exceptions import ApplicationAlreadyExists
from app.applications.domain.models.application import Application
from app.applications.domain.repositories import ApplicationRepository
from app.applications.infrastructure.persistence.models.orm_application import (
    ORMEventApplication,
)
from app.events.domain.models.event import Event
from app.events.infrastructure.persistence.models.orm_event import ORMEvent
from app.users.domain.models.user import User, UserRoles
from app.users.infrastructure.persistence.models.orm_user import ORMUser


class ORMApplicationRepository(ApplicationRepository):
    def create(self, application: Application) -> None:
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

    def get_by_user(self, user: User) -> List[Application]:
        user_orm = ORMUser.objects.get(id=user.id)

        return [
            self._to_domain_model(application)
            for application in ORMEventApplication.objects.filter(user=user_orm)
        ]

    def get_by_event(self, event_id: uuid.UUID) -> List[Application]:
        event_orm = ORMEvent.objects.get(id=event_id)

        return [
            self._to_domain_model(application)
            for application in ORMEventApplication.objects.filter(event=event_orm)
        ]

    def _to_domain_model(self, orm_application: ORMEventApplication) -> Application:
        return Application(
            id=orm_application.id,
            user=User(
                id=orm_application.user.id,
                email=orm_application.user.email,
                password=orm_application.user.password,
                first_name=orm_application.user.first_name,
                last_name=orm_application.user.last_name,
                username=orm_application.user.username,
                bio=orm_application.user.bio,
                profile_image=orm_application.user.profile_image,
                role=UserRoles[orm_application.user.role],
                created_at=orm_application.user.created_at,
                updated_at=orm_application.user.updated_at,
                date_of_birth=orm_application.user.date_of_birth,
                study=orm_application.user.study,
                work=orm_application.user.work,
            ),
            event=Event(
                id=orm_application.event.id,
                name=orm_application.event.name,
                description=orm_application.event.description,
                url=orm_application.event.url,
                start_date=orm_application.event.start_date,
                end_date=orm_application.event.end_date,
                location=orm_application.event.location,
                header_image=orm_application.event.header_image,
                created_at=orm_application.event.created_at,
                updated_at=orm_application.event.updated_at,
                deleted_at=orm_application.event.deleted_at,
            ),
            created_at=orm_application.created_at,
            updated_at=orm_application.updated_at,
            deleted_at=orm_application.deleted_at,
        )
