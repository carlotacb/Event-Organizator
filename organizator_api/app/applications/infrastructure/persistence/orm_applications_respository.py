import uuid
from typing import List

from django.db import IntegrityError

from app.applications.domain.exceptions import (
    ApplicationAlreadyExists,
    ApplicationNotFound,
)
from app.applications.domain.models.application import Application, ApplicationStatus
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
            for application in ORMEventApplication.objects.filter(
                user=user_orm
            ).order_by("-event__start_date")
        ]

    def get_by_event(self, event_id: uuid.UUID) -> List[Application]:
        event_orm = ORMEvent.objects.get(id=event_id)

        return [
            self._to_domain_model(application)
            for application in ORMEventApplication.objects.filter(event=event_orm)
        ]

    def get_application(self, event_id: uuid.UUID, user_id: uuid.UUID) -> Application:
        event_orm = ORMEvent.objects.get(id=event_id)
        user_orm = ORMUser.objects.get(id=user_id)

        try:
            return self._to_domain_model(
                ORMEventApplication.objects.get(event=event_orm, user=user_orm)
            )
        except ORMEventApplication.DoesNotExist:
            raise ApplicationNotFound

    def get(self, application_id: uuid.UUID) -> Application:
        try:
            return self._to_domain_model(
                ORMEventApplication.objects.get(id=application_id)
            )
        except ORMEventApplication.DoesNotExist:
            raise ApplicationNotFound

    def update(self, application: Application) -> None:
        try:
            orm_application = ORMEventApplication.objects.get(id=application.id)
            orm_application.status = ApplicationStatus(application.status).name
            orm_application.updated_at = application.updated_at
            orm_application.save()
        except ORMEventApplication.DoesNotExist:
            raise ApplicationNotFound

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
                token=orm_application.user.token,
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
                open_for_participants=orm_application.event.open_for_participants,
                max_participants=orm_application.event.max_participants,
                expected_attrition_rate=orm_application.event.expected_attrition_rate,
                students_only=orm_application.event.students_only,
                age_restrictions=orm_application.event.age_restrictions,
            ),
            status=ApplicationStatus[orm_application.status],
            created_at=orm_application.created_at,
            updated_at=orm_application.updated_at,
        )
