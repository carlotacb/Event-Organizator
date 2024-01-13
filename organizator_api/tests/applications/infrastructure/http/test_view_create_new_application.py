import json
import uuid
from datetime import datetime

from app.users.domain.models.user import UserRoles, GenderOptions, TShirtSizes
from tests.api_tests import ApiTests
from tests.events.domain.EventFactory import EventFactory
from tests.users.domain.UserFactory import UserFactory


class TestViewCreateNewApplication(ApiTests):
    def setUp(self) -> None:
        super().setUp()
        self.user_repository.clear()
        self.user_token_participant = "baad2fe5-0122-459b-9572-625c3351d6ac"
        user = UserFactory().create(
            token=uuid.UUID(self.user_token_participant),
            role=UserRoles.PARTICIPANT,
            gender=GenderOptions.FEMALE,
            tshirt=TShirtSizes.M,
            alimentary_restrictions="No restrictions",
            username="charlie",
            email="charlie@test.com",
        )
        self.user_repository.create(user)

        self.event_repository.clear()
        self.correct_event_id = "fbce7302-68b2-48d3-9030-f6c56fcacf10"
        event = EventFactory().create(new_id=uuid.UUID(self.correct_event_id))
        self.event_repository.create(event)

        self.application_repository.clear()

    def test__given_a_valid_event_id__when_create_application_without_header__then_unauthorized_is_returned(
        self,
    ) -> None:
        # Given
        body = {"event_id": self.correct_event_id}

        # When
        response = self.client.post(
            "/organizator-api/applications/new",
            json.dumps(body),
            content_type="application/json",
        )

        # Then
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.content, b"Unauthorized")

    def test__given_a_valid_event_id__when_create_application_with_invalid_token__then_invalid_token_is_returned(
        self,
    ) -> None:
        # Given
        body = {"event_id": self.correct_event_id}

        # When
        headers = {"HTTP_Authorization": "invalid_token"}
        response = self.client.post(
            "/organizator-api/applications/new",
            json.dumps(body),
            content_type="application/json",
            **headers  # type: ignore
        )

        # Then
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b"Invalid token")

    def test__given_a_body_without_event_id__when_create_application__then_event_id_is_required_is_returned(
        self,
    ) -> None:
        # Given
        body = {"event": "this_is_not_an_event_id"}

        # When
        headers = {"HTTP_Authorization": self.user_token_participant}
        response = self.client.post(
            "/organizator-api/applications/new",
            json.dumps(body),
            content_type="application/json",
            **headers  # type: ignore
        )

        # Then
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.content, b"Event id is required")

    def test__given_no_exiting_user_id_db__when_create_application__then_user_not_found_is_returned(
        self,
    ) -> None:
        # Given
        body = {"event_id": self.correct_event_id}

        # When
        headers = {"HTTP_Authorization": "fef96ea6-6441-4bea-90d5-8398b892d233"}
        response = self.client.post(
            "/organizator-api/applications/new",
            json.dumps(body),
            content_type="application/json",
            **headers  # type: ignore
        )

        # Then
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content, b"User not found")

    def test__given_a_correct_event_id_and_a_incomplete_user_in_db__when_create_application__then_event_profile_not_complete_is_returned(
        self,
    ) -> None:
        # Given
        user_token = "03c8bcb7-6c6f-4362-8dbf-6c8b191bb5d3"
        user = UserFactory().create(
            token=uuid.UUID(user_token), role=UserRoles.PARTICIPANT
        )
        self.user_repository.create(user)

        body = {"event_id": self.correct_event_id}

        # When
        headers = {"HTTP_Authorization": user_token}
        response = self.client.post(
            "/organizator-api/applications/new",
            json.dumps(body),
            content_type="application/json",
            **headers  # type: ignore
        )

        # Then
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.content, b"Profile not complete")

    def test__given_no_existing_event_in_db_and_complete_user__when_create_application__then_event_not_found_is_returned(
        self,
    ) -> None:
        # Given
        event_id = "e244bf58-422b-4a47-b9e7-a883a8cbb809"
        body = {"event_id": event_id}

        # When
        headers = {"HTTP_Authorization": self.user_token_participant}
        response = self.client.post(
            "/organizator-api/applications/new",
            json.dumps(body),
            content_type="application/json",
            **headers  # type: ignore
        )

        # Then
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content, b"Event not found")

    def test__given_a_correct_event_id_and_a_complete_user__when_create_application_a_application_2_times__then_application_already_exists_is_returned(
        self,
    ) -> None:
        # Given
        body = {"event_id": self.correct_event_id}

        # When
        headers = {"HTTP_Authorization": self.user_token_participant}
        self.client.post(
            "/organizator-api/applications/new",
            json.dumps(body),
            content_type="application/json",
            **headers  # type: ignore
        )
        response = self.client.post(
            "/organizator-api/applications/new",
            json.dumps(body),
            content_type="application/json",
            **headers  # type: ignore
        )

        # Then
        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.content, b"Application already exists")

    def test__given_a_correct_event_id_and_a_complete_organizer_user__when_create_application__then_you_should_have_role_participant_to_apply_is_returned(
        self,
    ) -> None:
        # Given
        user_token = "03c8bcb7-6c6f-4362-8dbf-6c8b191bb5d3"
        user = UserFactory().create(
            token=uuid.UUID(user_token),
            role=UserRoles.ORGANIZER,
            tshirt=TShirtSizes.M,
            gender=GenderOptions.FEMALE,
            alimentary_restrictions="No restrictions",
        )
        self.user_repository.create(user)

        body = {"event_id": self.correct_event_id}

        # When
        headers = {"HTTP_Authorization": user_token}
        response = self.client.post(
            "/organizator-api/applications/new",
            json.dumps(body),
            content_type="application/json",
            **headers  # type: ignore
        )

        # Then
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.content, b"You should have role participant to apply")

    def test__given_a_correct_event_id_and_a_complete_user_without_study__when_create_application__then_you_should_be_student_to_apply_is_returned(
        self,
    ) -> None:
        # Given
        user_token = "03c8bcb7-6c6f-4362-8dbf-6c8b191bb5d3"
        user = UserFactory().create(
            token=uuid.UUID(user_token),
            study=False,
            tshirt=TShirtSizes.M,
            gender=GenderOptions.FEMALE,
            alimentary_restrictions="No restrictions",
        )
        self.user_repository.create(user)

        body = {"event_id": self.correct_event_id}

        # When
        headers = {"HTTP_Authorization": user_token}
        response = self.client.post(
            "/organizator-api/applications/new",
            json.dumps(body),
            content_type="application/json",
            **headers  # type: ignore
        )

        # Then
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.content, b"You should be student to apply")

    def test__given_a_correct_event_id_and_a_user_too_young__when_create_application__then_you_are_too_young_to_apply(
        self,
    ) -> None:
        # Given
        user_token = "03c8bcb7-6c6f-4362-8dbf-6c8b191bb5d3"
        user = UserFactory().create(
            token=uuid.UUID(user_token),
            date_of_birth=datetime(2010, 1, 1),
            tshirt=TShirtSizes.M,
            gender=GenderOptions.FEMALE,
            alimentary_restrictions="No restrictions",
        )
        self.user_repository.create(user)

        body = {"event_id": self.correct_event_id}

        # When
        headers = {"HTTP_Authorization": user_token}
        response = self.client.post(
            "/organizator-api/applications/new",
            json.dumps(body),
            content_type="application/json",
            **headers  # type: ignore
        )

        # Then
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.content, b"You are too young to apply")

    def test__given_a_correct_id_for_a_already_started_event_and_a_complete_user__when_create_application__then_event_already_started_is_returned(
        self,
    ) -> None:
        # Given
        event_id = "fbce7302-68b2-48d3-9030-f6c56fcacf10"
        event = EventFactory().create(
            new_id=uuid.UUID(event_id),
            start_date=datetime(2020, 1, 1),
            name="HackUPC 2024",
        )
        self.event_repository.create(event)

        body = {"event_id": event_id}

        # When
        headers = {"HTTP_Authorization": self.user_token_participant}
        response = self.client.post(
            "/organizator-api/applications/new",
            json.dumps(body),
            content_type="application/json",
            **headers  # type: ignore
        )

        # Then
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.content, b"Event already started")

    def test__given_a_correct_event_id_and_a_complete_user__when_create_application__then_application_created_correctly_is_returned(
        self,
    ) -> None:
        # Given
        body = {"event_id": self.correct_event_id}

        # When
        headers = {"HTTP_Authorization": self.user_token_participant}
        response = self.client.post(
            "/organizator-api/applications/new",
            json.dumps(body),
            content_type="application/json",
            **headers  # type: ignore
        )

        # Then
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.content, b"Application created correctly")
