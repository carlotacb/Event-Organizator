import uuid

from app.questions.domain.usecases.get_question_by_id_use_case import (
    GetQuestionsByIdUseCase,
)
from tests.api_tests import ApiTests
from tests.events.domain.EventFactory import EventFactory
from tests.questions.domain.QuestionFactory import QuestionFactory
from tests.users.domain.UserFactory import UserFactory


class TestGetQuestionByIdUseCase(ApiTests):
    def setUp(self) -> None:
        super().setUp()
        self.event_repository.clear()
        self.question_repository.clear()

        self.event_id = uuid.UUID("eb41b762-5988-4fa3-8942-7a91ccb00686")
        event = EventFactory().create(new_id=self.event_id)
        self.event_repository.create(event)

        question = QuestionFactory().create(
            new_id=uuid.UUID("eb41b762-5988-4fa3-8942-7a91ccb00686"),
            event=event,
        )
        self.question_repository.create(question)

        self.token = uuid.UUID("eb41b762-5988-4fa3-8942-7a91ccb00686")
        user_complete = UserFactory().create(
            token=self.token,
        )
        self.user_repository.create(user_complete)

    def test__given_questions_in_db__when_get_question_by_id__then_question_is_returned(
        self,
    ) -> None:
        # Given
        question_id = uuid.UUID("eb41b762-5988-4fa3-8942-7a91ccb00686")

        # When
        question = GetQuestionsByIdUseCase().execute(question_id=question_id)

        # Then
        self.assertEqual(question_id, question.id)
        self.assertEqual("Question", question.question)
