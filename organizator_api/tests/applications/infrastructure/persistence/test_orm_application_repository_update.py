import uuid
from datetime import datetime, timezone

from app.applications.domain.exceptions import ApplicationNotFound
from app.applications.domain.models.application import Application, ApplicationStatus
from app.applications.infrastructure.persistence.orm_applications_respository import (
    ORMApplicationRepository,
)
from tests.api_tests import ApiTests


class TestORMApplicationRepositoryUpdate(ApiTests):
    def test_given_a_non_existing_application_in_db__when_update__then_raise_application_not_found(
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
            id=uuid.UUID("ef6f6fb3-ba46-43dd-a0da-95de8125b1cc"),
            user=user,
            event=event,
            status=ApplicationStatus.PENDING,
            created_at=datetime.now(tz=timezone.utc),
            updated_at=datetime.now(tz=timezone.utc),
        )

        # When / Then
        with self.assertRaises(ApplicationNotFound):
            ORMApplicationRepository().update(application=application)

    def test__given_a_existing_application_in_db__when_update__then_the_application_is_updated(
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
            id=uuid.UUID("ef6f6fb3-ba46-43dd-a0da-95de8125b1cc"),
            user=user,
            event=event,
            status=ApplicationStatus.PENDING,
            created_at=datetime.now(tz=timezone.utc),
            updated_at=datetime.now(tz=timezone.utc),
        )

        ORMApplicationRepository().create(application=application)

        # When
        application.status = ApplicationStatus.INVITED
        ORMApplicationRepository().update(application=application)

        # Then
        response = ORMApplicationRepository().get(application_id=application.id)
        self.assertEqual(response.status, ApplicationStatus.INVITED)
