import uuid

from app.answers.application.request import CreateAnswerRequest
from app.answers.domain.usecases.create_answer_use_case import CreateAnswerUseCase
from tests.api_tests import ApiTests
from tests.applications.domain.ApplicationFactory import ApplicationFactory
from tests.events.domain.EventFactory import EventFactory
from tests.questions.domain.QuestionFactory import QuestionFactory
from tests.users.domain.UserFactory import UserFactory


class TestCreateAnswerUseCase(ApiTests):

    def setUp(self) -> None:
        super().setUp()
        self.event_repository.clear()
        self.application_repository.clear()
        self.question_repository.clear()
        self.answer_repository.clear()

        self.user_token_participant = uuid.UUID("eb41b762-5988-4fa3-8942-7a91ccb00686")
        self.user_participant = UserFactory().create(
            new_id=uuid.UUID("eb41b762-5988-4fa3-8942-7a91ccb00686"),
            token=self.user_token_participant,
            username="john",
            email="john@test.com",
        )
        self.user_repository.create(self.user_participant)

        self.event_id = uuid.UUID("eb41b762-5988-4fa3-8942-7a91ccb00686")
        self.event = EventFactory().create(new_id=self.event_id)
        self.event_repository.create(self.event)

        self.question = QuestionFactory().create(
            new_id=uuid.UUID("eb41b762-5988-4fa3-8942-7a91ccb00686"),
            event=self.event,
        )
        self.question_repository.create(self.question)

        self.application = ApplicationFactory().create(
            new_id=uuid.UUID("eb41b762-5988-4fa3-8942-7a91ccb00686"),
            user=self.user_participant,
            event=self.event,
        )
        self.application_repository.create(self.application)

    def test__given_an_application_and_a_question__when_create_answer__then_answer_is_created(self) -> None:
        # Given
        answer_data = CreateAnswerRequest(
            application_id=self.application.id,
            question_id=self.question.id,
            answer="this is the answer",
        )

        # When
        CreateAnswerUseCase().execute(answer_data=answer_data)

        # Then
        self.assertEqual(1, len(self.answer_repository.get_all()))


