import uuid
from datetime import timezone, datetime

from app.applications.domain.models.application import Application, ApplicationStatus
from app.applications.infrastructure.persistence.orm_applications_respository import (
    ORMApplicationRepository,
)
from tests.api_tests import ApiTests


class TestORMApplicationRepositoryGetByUser(ApiTests):
    def test__given_no_applications_for_the_user__when_get_by_user__then_return_empty_list(
        self,
    ) -> None:
        # Given
        user = self.given_user_in_orm(
            new_id=uuid.UUID("ef6f6fb3-ba12-43dd-a0da-95de8125b1cc"),
            username="john",
            email="john@test.com",
        )

        # When
        response = ORMApplicationRepository().get_by_user(user=user)

        # Then
        self.assertEqual([], response)

    def test__given_a_application_for_the_user__when_get_by_user__then_return_the_application(
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
        response = ORMApplicationRepository().get_by_user(user=user)

        # Then
        self.assertEqual(1, len(response))
        self.assertEqual(application.id, response[0].id)
        self.assertEqual(application.user.id, response[0].user.id)
        self.assertEqual(application.event.id, response[0].event.id)
        self.assertEqual(application.status, response[0].status)
        self.assertEqual(application.created_at, response[0].created_at)
        self.assertEqual(application.updated_at, response[0].updated_at)

    def test__given_a_application_for_the_user_and_another_application_for_another_user__when_get_by_user__then_return_the_application(
        self,
    ) -> None:
        # Given
        user = self.given_user_in_orm(
            new_id=uuid.UUID("ef6f6fb3-ba12-43dd-a0da-95de8125b1cc"),
            username="john",
            email="john@test.com",
        )
        user2 = self.given_user_in_orm(
            new_id=uuid.UUID("ef6f6fb3-ba14-43dd-a0da-95de8125b1cc"),
            username="jane",
            email="jane@test.com",
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

        application2 = Application(
            id=uuid.UUID("ef6f6fb3-ba46-43dd-a0da-95de8125b1cd"),
            user=user2,
            event=event,
            status=ApplicationStatus.PENDING,
            created_at=datetime.now(tz=timezone.utc),
            updated_at=datetime.now(tz=timezone.utc),
        )

        ORMApplicationRepository().create(application=application)
        ORMApplicationRepository().create(application=application2)

        # When
        response = ORMApplicationRepository().get_by_user(user=user)

        # Then
        self.assertEqual(1, len(response))
        self.assertEqual(application.id, response[0].id)
        self.assertEqual(application.user.id, response[0].user.id)
        self.assertEqual(application.event.id, response[0].event.id)
        self.assertEqual(application.status, response[0].status)
        self.assertEqual(application.created_at, response[0].created_at)
        self.assertEqual(application.updated_at, response[0].updated_at)
