import uuid

from app.users.domain.models.user import GenderOptions, TShirtSizes
from tests.answers.domain.AnswerFactory import AnswerFactory
from tests.api_tests import ApiTests
from tests.applications.domain.ApplicationFactory import ApplicationFactory
from tests.events.domain.EventFactory import EventFactory
from tests.questions.domain.QuestionFactory import QuestionFactory
from tests.users.domain.UserFactory import UserFactory


class TestViewGetAnswersById(ApiTests):
    def setUp(self) -> None:
        super().setUp()
        self.question_repository.clear()
        self.user_repository.clear()
        self.event_repository.clear()
        self.application_repository.clear()

        self.event = EventFactory().create(
            new_id=uuid.UUID("eb41b762-5988-4fa3-8942-7a91ccb00686")
        )
        self.event_repository.create(self.event)

        self.user_token = "baad2fe5-0122-459b-9572-625c3351d6ac"
        self.user = UserFactory().create(
            token=uuid.UUID(self.user_token),
            tshirt=TShirtSizes.M,
            gender=GenderOptions.FEMALE,
            alimentary_restrictions="No restrictions",
            username="charlie",
            email="charlie@test.com",
        )
        self.user_repository.create(self.user)

        self.question_id = "eb41b762-5988-4fa3-8942-7a91ccb00686"
        self.question = QuestionFactory().create(
            new_id=uuid.UUID(self.question_id),
            event=self.event,
        )
        self.question_repository.create(self.question)

        self.application_id = "eb41b762-5988-4fa3-8942-7a91ccb00686"
        self.application = ApplicationFactory().create(
            new_id=uuid.UUID(self.application_id),
            user=self.user,
            event=self.event,
        )
        self.application_repository.create(self.application)

    def test__when_get_answers_by_id_without_header__then_unauthorized_is_returned(
        self,
    ) -> None:
        # When
        response = self.client.get(
            "/organizator-api/answers/application/eb41b762-5988-4fa3-8942-7a91ccb00686",
            content_type="application/json",
        )

        # Then
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.content, b"Unauthorized")

    def test__when_get_answers_by_id_with_invalid_token__then_bad_request_is_returned(
        self,
    ) -> None:
        # When
        headers = {"HTTP_Authorization": "invalid_token"}
        response = self.client.get(
            "/organizator-api/answers/application/eb41b762-5988-4fa3-8942-7a91ccb00686",
            content_type="application/json",
            **headers  # type: ignore
        )

        # Then
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b"Invalid token")

    def test__when_get_answers_by_id_with_invalid_application_id__then_not_found_is_returned(
        self,
    ) -> None:
        # When
        headers = {"HTTP_Authorization": self.user_token}
        response = self.client.get(
            "/organizator-api/answers/application/eb41b762-5988-4fa3-8945-7a91ccb00686",
            content_type="application/json",
            **headers  # type: ignore
        )

        # Then
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content, b"Application not found")

    def test__when_get_answers_by_id_from_a_user_that_is_not_the_author__then_user_not_author_is_returned(
        self,
    ) -> None:
        # Given
        user_token = "baad2fe5-0122-459b-9872-625c3351d6ac"
        user = UserFactory().create(
            new_id=uuid.UUID(user_token),
            token=uuid.UUID(user_token),
            tshirt=TShirtSizes.M,
            gender=GenderOptions.FEMALE,
            alimentary_restrictions="No restrictions",
            username="carlotaaaa",
            email="charliaaa@test.com",
        )
        self.user_repository.create(self.user)

        # When
        headers = {"HTTP_Authorization": user_token}
        response = self.client.get(
            "/organizator-api/answers/application/eb41b762-5988-4fa3-8942-7a91ccb00686",
            content_type="application/json",
            **headers  # type: ignore
        )

        # Then
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.content, b"User is not author of answer")

    def test__when_get_answers_by_id_with_valid_application_id__then_answers_are_returned(
        self,
    ) -> None:
        # Given
        answer = AnswerFactory().create(
            application=self.application,
            question=self.question,
            answer="Answer",
        )
        self.answer_repository.create(answer)

        # When
        headers = {"HTTP_Authorization": self.user_token}
        response = self.client.get(
            "/organizator-api/answers/application/eb41b762-5988-4fa3-8942-7a91ccb00686",
            content_type="application/json",
            **headers  # type: ignore
        )

        # Then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.content,
            b'[{"id": "eb41b762-5988-4fa3-8942-7a91ccb00686", "question_id": "eb41b762-5988-4fa3-8942-7a91ccb00686", "question": "Question", "answer": "Answer"}]',
        )
