import uuid
from datetime import datetime, timezone

from app.applications.domain.exceptions import ApplicationNotFound
from app.applications.domain.models.application import Application, ApplicationStatus
from app.applications.infrastructure.persistence.orm_applications_respository import (
    ORMApplicationRepository,
)
from tests.api_tests import ApiTests


class TestORMApplicationRepositoryGetApplication(ApiTests):
    def test__given_no_applications_for_the_event_and_user__when_get_application__then_raise_application_not_found(
        self,
    ) -> None:
        # Given
        self.given_user_in_orm(
            new_id=uuid.UUID("ef6f6fb3-ba12-43dd-a0da-95de8125b1cc"),
            username="john",
            email="john@test.com",
        )
        self.given_event_in_orm(
            new_id=uuid.UUID("ef6f6fb3-ba46-43dd-a0da-95de8125b1cc"), name="event"
        )

        # When / Then
        with self.assertRaises(ApplicationNotFound):
            ORMApplicationRepository().get_application(
                event_id=uuid.UUID("ef6f6fb3-ba46-43dd-a0da-95de8125b1cc"),
                user_id=uuid.UUID("ef6f6fb3-ba12-43dd-a0da-95de8125b1cc"),
            )

    def test__given_a_application_for_the_event_and_user__when_get_application__then_return_the_application(
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
        response = ORMApplicationRepository().get_application(
            event_id=event.id, user_id=user.id
        )

        # Then
        self.assertEqual(application.id, response.id)
        self.assertEqual(application.user.id, response.user.id)
        self.assertEqual(application.event.id, response.event.id)
        self.assertEqual(application.status, response.status)
        self.assertEqual(application.created_at, response.created_at)
        self.assertEqual(application.updated_at, response.updated_at)
