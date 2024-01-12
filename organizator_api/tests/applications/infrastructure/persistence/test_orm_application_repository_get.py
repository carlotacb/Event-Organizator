import uuid
from datetime import datetime, timezone

from app.applications.domain.exceptions import ApplicationNotFound
from app.applications.domain.models.application import ApplicationStatus, Application
from app.applications.infrastructure.persistence.orm_applications_respository import (
    ORMApplicationRepository,
)
from tests.api_tests import ApiTests


class TestORMApplicationRepositoryGet(ApiTests):
    def test__given_a_non_existing_application_id__when_get__then_raise_application_not_found(
        self,
    ) -> None:
        # When / Then
        with self.assertRaises(ApplicationNotFound):
            ORMApplicationRepository().get(application_id=uuid.uuid4())

    def test__given_a_existing_application_id__when_get__then_return_the_application(
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
        response = ORMApplicationRepository().get(application_id=application.id)

        # Then
        self.assertEqual(response.id, application.id)
        self.assertEqual(response.user.id, application.user.id)
        self.assertEqual(response.event.id, application.event.id)
        self.assertEqual(response.status, application.status)
