import uuid

from app.questions.domain.models.question import QuestionType
from app.users.domain.models.user import UserRoles
from tests.api_tests import ApiTests
from tests.events.domain.EventFactory import EventFactory
from tests.questions.domain.QuestionFactory import QuestionFactory
from tests.users.domain.UserFactory import UserFactory


class TestViewGetQuestionsByEvent(ApiTests):
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

    def test__when_get_questions_by_event_without_header__then_unauthorized_is_returned(
        self,
    ) -> None:
        # When
        response = self.client.get(
            "/organizator-api/questions/event/eb41b762-5988-4fa3-8942-7a91ccb00686",
            content_type="application/json",
        )

        # Then
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.content, b"Unauthorized")

    def test__when_get_questions_by_event_with_invalid_token__then_invalid_token_is_returned(
        self,
    ) -> None:
        # When
        headers = {"HTTP_Authorization": "invalid_token"}
        response = self.client.get(
            "/organizator-api/questions/event/eb41b762-5988-4fa3-8942-7a91ccb00686",
            content_type="application/json",
            **headers  # type: ignore
        )

        # Then
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b"Invalid token")

    def test__when_get_questions_by_event_with_a_not_logged_in_token__then_questions_are_returned(
        self,
    ) -> None:
        # When
        headers = {"HTTP_Authorization": "eb41b762-5988-4fa3-8942-7a91ccb00686"}
        response = self.client.get(
            "/organizator-api/questions/event/eb41b762-5988-4fa3-8942-7a91ccb00686",
            content_type="application/json",
            **headers  # type: ignore
        )

        # Then
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.content, b"User not logged in")

    def test__when_get_questions_by_event_with_a_logged_in_token__then_questions_are_returned(
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

        # When
        headers = {"HTTP_Authorization": self.user_token_participant}
        response = self.client.get(
            "/organizator-api/questions/event/eb41b762-5988-4fa3-8942-7a91ccb00686",
            content_type="application/json",
            **headers  # type: ignore
        )

        # Then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.content,
            b'[{"id": "eb41b762-5988-4fa3-8942-7a91ccb00686", "question": "What is your favourite color?", "question_type": "Options", "options": "Red, Blue, Green"}]',
        )
