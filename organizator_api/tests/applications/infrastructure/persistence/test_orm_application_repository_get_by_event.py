import uuid
from datetime import datetime, timezone

from app.applications.domain.models.application import Application
from app.applications.infrastructure.persistence.orm_applications_respository import (
    ORMApplicationRepository,
)
from tests.api_tests import ApiTests


class TestORMApplicationRepositoryGetByEvent(ApiTests):
    def test__given_no_applications_for_the_event__when_get_by_event__then_return_empty_list(
        self,
    ) -> None:
        # Given
        event = self.given_event_in_orm(
            new_id=uuid.UUID("ef6f6fb3-ba12-43dd-a0da-95de8125b1cc"), name="event"
        )

        # When
        response = ORMApplicationRepository().get_by_event(event_id=event.id)

        # Then
        self.assertEqual([], response)

    def test__given_a_application_for_the_event__when_get_by_event__then_return_the_application(
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
            created_at=datetime.now(tz=timezone.utc),
            updated_at=datetime.now(tz=timezone.utc),
        )

        ORMApplicationRepository().create(application=application)

        # When
        response = ORMApplicationRepository().get_by_event(event_id=event.id)

        # Then
        self.assertEqual(1, len(response))
        self.assertEqual(application.id, response[0].id)
        self.assertEqual(application.user.id, response[0].user.id)
        self.assertEqual(application.event.id, response[0].event.id)
        self.assertEqual(application.created_at, response[0].created_at)
        self.assertEqual(application.updated_at, response[0].updated_at)
