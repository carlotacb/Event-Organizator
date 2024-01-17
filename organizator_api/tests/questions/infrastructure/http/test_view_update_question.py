import uuid

from app.questions.domain.models.question import QuestionType
from app.users.domain.models.user import GenderOptions, UserRoles, TShirtSizes
from tests.api_tests import ApiTests
from tests.events.domain.EventFactory import EventFactory
from tests.questions.domain.QuestionFactory import QuestionFactory
from tests.users.domain.UserFactory import UserFactory


class TestViewUpdateQuestion(ApiTests):
    def setUp(self) -> None:
        super().setUp()
        self.question_repository.clear()
        self.user_repository.clear()
        self.event_repository.clear()

        self.event_id = "eb41b762-5988-4fa3-8942-7a91ccb00686"
        self.event = EventFactory().create(new_id=uuid.UUID(self.event_id))
        self.event_repository.create(self.event)

        self.user_token_participant = "baad2fe5-0122-459b-9572-625c3351d6ac"
        user = UserFactory().create(
            token=uuid.UUID(self.user_token_participant),
            role=UserRoles.PARTICIPANT,
            username="charlie",
            email="charlie@test.com",
        )
        self.user_repository.create(user)

        self.user_token_organizer = "baad2fe5-0122-459b-9572-625c3351d6cc"
        user2 = UserFactory().create(
            new_id=uuid.UUID("baad2fe5-0122-459b-9575-625c3351d6cc"),
            token=uuid.UUID(self.user_token_organizer),
            role=UserRoles.ORGANIZER_ADMIN,
        )
        self.user_repository.create(user2)

    def test__when_update_question_without_header__then_unauthorized_is_returned(
        self,
    ) -> None:
        # When
        response = self.client.post(
            "/organizator-api/questions/update/eb41b762-5988-4fa3-8942-7a91ccb00686",
            content_type="application/json",
        )

        # Then
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.content, b"Unauthorized")

    def test__when_update_question_with_invalid_token__then_invalid_token_is_returned(
        self,
    ) -> None:
        # When
        headers = {"HTTP_Authorization": "invalid_token"}
        response = self.client.post(
            "/organizator-api/questions/update/eb41b762-5988-4fa3-8942-7a91ccb00686",
            content_type="application/json",
            **headers  # type: ignore
        )

        # Then
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b"Invalid token")

    def test__given_a_participant_user__when_update_question__then_only_organizer_admins_can_update_questions(
        self,
    ) -> None:
        # When
        headers = {"HTTP_Authorization": self.user_token_participant}
        response = self.client.post(
            "/organizator-api/questions/update/eb41b762-5988-4fa3-8942-7a91ccb00686",
            content_type="application/json",
            **headers  # type: ignore
        )

        # Then
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.content, b"Only organizer admins can update questions"
        )

    def test__given_a_valid_body__when_update_un_existing_question__then_question_does_not_exist_is_returned(
        self,
    ) -> None:
        # Given
        body = {
            "question": "What is your favourite color?",
            "question_type": "OPTIONS",
            "options": ["Red", "Blue", "Green"],
        }

        # When
        headers = {"HTTP_Authorization": self.user_token_organizer}
        response = self.client.post(
            "/organizator-api/questions/update/eb41b762-5988-4fa3-8942-7a91ccb00686",
            content_type="application/json",
            data=body,
            **headers  # type: ignore
        )

        # Then
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content, b"Question does not exist")

    def test__given_a_valid_body__when_update_question__then_question_is_updated(
        self,
    ) -> None:
        # Given
        question = QuestionFactory().create(
            new_id=uuid.UUID("eb41b762-5988-4fa3-8942-7a91ccb00686"),
            question="What is your favourite color?",
            question_type=QuestionType.OPTIONS,
            options="Red, Blue, Green",
            event=self.event,
        )
        self.question_repository.create(question)
        body = {
            "question": "What is your color?",
        }

        # When
        headers = {"HTTP_Authorization": self.user_token_organizer}
        response = self.client.post(
            "/organizator-api/questions/update/eb41b762-5988-4fa3-8942-7a91ccb00686",
            content_type="application/json",
            data=body,
            **headers  # type: ignore
        )

        # Then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"Question updated correctly")
