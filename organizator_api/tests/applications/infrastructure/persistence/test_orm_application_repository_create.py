import uuid
from datetime import datetime, timezone

from app.applications.domain.exceptions import ApplicationAlreadyExists
from app.applications.domain.models.application import Application, ApplicationStatus
from app.applications.infrastructure.persistence.models.orm_application import (
    ORMEventApplication,
)
from app.applications.infrastructure.persistence.orm_applications_respository import (
    ORMApplicationRepository,
)
from app.events.domain.exceptions import EventNotFound
from tests.api_tests import ApiTests


class TestORMApplicationRepositoryCreate(ApiTests):
    def test__given_a_application_with_a_valid_user_and_event__when_create__then_application_is_saved(
        self,
    ) -> None:
        # Given
        user = self.given_user_in_orm(
            new_id=uuid.UUID("ef6f6fb3-ba12-43dd-a0da-95de8125b1cc"),
            username="john",
            email="john@test.com",
        )
        event = self.given_event_in_orm(
            new_id=uuid.UUID("ef6f6fb3-ba46-43dd-a0da-95de8125b1cc"), name="event"
        )
        application = Application(
            id=uuid.UUID("ef6f6fb3-ba12-43dd-a0da-95de8125b1cc"),
            user=user,
            event=event,
            status=ApplicationStatus.PENDING,
            created_at=datetime.now(tz=timezone.utc),
            updated_at=datetime.now(tz=timezone.utc),
        )

        # When
        ORMApplicationRepository().create(application=application)

        # Then
        self.assertIsNotNone(ORMEventApplication.objects.get(id=str(application.id)))

    def test__given_a_application_in_orm_and_another_application_with_the_same_event_and_user__when_create__then_raise_application_already_exists(
        self,
    ) -> None:
        # Given
        user = self.given_user_in_orm(
            new_id=uuid.UUID("ef6f6fb3-ba12-43dd-a0da-95de8125b1cc"),
            username="john",
            email="john@test.com",
        )
        event = self.given_event_in_orm(
            new_id=uuid.UUID("ef6f6fb3-ba46-43dd-a0da-95de8125b1cc"), name="event"
        )
        application = Application(
            id=uuid.UUID("ef6f6fb3-ba12-43dd-a0da-95de8125b1cc"),
            user=user,
            event=event,
            status=ApplicationStatus.PENDING,
            created_at=datetime.now(tz=timezone.utc),
            updated_at=datetime.now(tz=timezone.utc),
        )
        ORMApplicationRepository().create(application=application)

        application2 = Application(
            id=uuid.UUID("ef6f6fb3-ba14-43dd-a0da-95de8125b1cc"),
            user=user,
            event=event,
            status=ApplicationStatus.PENDING,
            created_at=datetime.now(tz=timezone.utc),
            updated_at=datetime.now(tz=timezone.utc),
        )

        # When / Then
        with self.assertRaises(ApplicationAlreadyExists):
            ORMApplicationRepository().create(application=application2)
