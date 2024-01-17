import json
import uuid

from app.users.domain.models.user import GenderOptions, UserRoles, TShirtSizes
from tests.api_tests import ApiTests
from tests.events.domain.EventFactory import EventFactory
from tests.users.domain.UserFactory import UserFactory


class TestViewCreateNewQuestion(ApiTests):
    def setUp(self) -> None:
        super().setUp()
        self.question_repository.clear()
        self.user_repository.clear()
        self.event_repository.clear()

        self.event_id = "eb41b762-5988-4fa3-8942-7a91ccb00686"
        event = EventFactory().create(new_id=uuid.UUID(self.event_id))
        self.event_repository.create(event)

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

        self.user_token_organizer = "baad2fe5-0122-459b-9572-625c3351d6cc"
        user2 = UserFactory().create(
            token=uuid.UUID(self.user_token_organizer),
            role=UserRoles.ORGANIZER_ADMIN,
            gender=GenderOptions.FEMALE,
            tshirt=TShirtSizes.M,
            alimentary_restrictions="No restrictions",
        )
        self.user_repository.create(user2)

    def test__when_create_question_without_header__then_unauthorized_is_returned(
        self,
    ) -> None:
        # When
        response = self.client.post(
            "/organizator-api/questions/new",
            content_type="application/json",
        )

        # Then
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.content, b"Unauthorized")

    def test__when_create_application_with_invalid_token__then_invalid_token_is_returned(
        self,
    ) -> None:
        # When
        headers = {"HTTP_Authorization": "invalid_token"}
        response = self.client.post(
            "/organizator-api/questions/new",
            content_type="application/json",
            **headers  # type: ignore
        )

        # Then
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b"Invalid token")

    def test__given_a_non_valid_event_id__when_create_question__then_event_id_is_invalid(
        self,
    ) -> None:
        # Given
        body = {"event_id": "invalid_event_id"}

        # When
        headers = {"HTTP_Authorization": self.user_token_organizer}
        response = self.client.post(
            "/organizator-api/questions/new",
            json.dumps(body),
            content_type="application/json",
            **headers  # type: ignore
        )

        # Then
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b"Invalid event id")

    def test__given_a_valid_event_id_and_with_not_all_the_parameters_in_the_body__when_create_question__then_question_created_correctly(
        self,
    ) -> None:
        # Given
        body = {"event_id": self.event_id}

        # When
        headers = {"HTTP_Authorization": self.user_token_organizer}
        response = self.client.post(
            "/organizator-api/questions/new",
            json.dumps(body),
            content_type="application/json",
            **headers  # type: ignore
        )

        # Then
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b"Unexpected body")

    def test__given_a_non_existing_event_id__when_create_question__then_event_does_not_exist(
        self,
    ) -> None:
        # Given
        body = {
            "event_id": "eb41b762-5988-4fa3-8942-7a91ccb00687",
            "question": "This is a question",
            "question_type": "TEXT",
            "options": "",
        }

        # When
        headers = {"HTTP_Authorization": self.user_token_organizer}
        response = self.client.post(
            "/organizator-api/questions/new",
            json.dumps(body),
            content_type="application/json",
            **headers  # type: ignore
        )

        # Then
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content, b"Event does not exist")

    def test__given_a_valid_event_id__when_create_question_with_participant_token__then_only_organizer_admin_can_create_questions(
        self,
    ) -> None:
        # Given
        body = {
            "event_id": self.event_id,
            "question": "This is a question",
            "question_type": "TEXT",
            "options": "",
        }

        # When
        headers = {"HTTP_Authorization": self.user_token_participant}
        response = self.client.post(
            "/organizator-api/questions/new",
            json.dumps(body),
            content_type="application/json",
            **headers  # type: ignore
        )

        # Then
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.content, b"Only organizer admins can create questions"
        )

    def test__given_a_valid_event_id__when_create_question_with_organizer_admin_token__then_question_created_correctly(
        self,
    ) -> None:
        # Given
        body = {
            "event_id": self.event_id,
            "question": "This is a question",
            "question_type": "TEXT",
            "options": "",
        }

        # When
        headers = {"HTTP_Authorization": self.user_token_organizer}
        response = self.client.post(
            "/organizator-api/questions/new",
            json.dumps(body),
            content_type="application/json",
            **headers  # type: ignore
        )

        # Then
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.content, b"Question created correctly")
