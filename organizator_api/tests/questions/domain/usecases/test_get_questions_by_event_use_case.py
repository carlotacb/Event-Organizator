import uuid

from app.questions.domain.usecases.get_questions_by_event_use_case import (
    GetQuestionsByEventUseCase,
)
from tests.api_tests import ApiTests
from tests.events.domain.EventFactory import EventFactory
from tests.questions.domain.QuestionFactory import QuestionFactory
from tests.users.domain.UserFactory import UserFactory


class TestGetQuestionsByEventUseCase(ApiTests):
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

        question2 = QuestionFactory().create(
            new_id=uuid.UUID("eb41b762-5988-4fa3-8943-7a91ccb00686"),
            event=event,
        )
        self.question_repository.create(question2)

        self.token = uuid.UUID("eb41b762-5988-4fa3-8942-7a91ccb00686")
        user_complete = UserFactory().create(
            token=self.token,
        )
        self.user_repository.create(user_complete)

    def test__given_a_non_existing_event__when_get_questions__then_a_empty_list_is_returned(
        self,
    ) -> None:
        # Given
        event_id = uuid.uuid4()

        # When
        questions = GetQuestionsByEventUseCase().execute(
            event_id=event_id, token=self.token
        )

        # Then
        self.assertEqual([], questions)

    def test__given_questions_in_the_db_for_a_existing_event__when_get_questions__then_a_list_with_the_questions_is_returned(
        self,
    ) -> None:
        # Given
        event_id = self.event_id

        # When
        questions = GetQuestionsByEventUseCase().execute(
            event_id=event_id, token=self.token
        )

        # Then
        self.assertEqual(2, len(questions))
        self.assertEqual("eb41b762-5988-4fa3-8942-7a91ccb00686", str(questions[0].id))
        self.assertEqual("eb41b762-5988-4fa3-8943-7a91ccb00686", str(questions[1].id))
