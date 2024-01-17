import uuid
from datetime import datetime, timezone

from app.questions.domain.models.question import Question, QuestionType
from app.questions.infrastructure.persistence.orm_questions_repository import (
    ORMQuestionRepository,
)
from tests.api_tests import ApiTests


class TestORMQuestionRepositoryGetAll(ApiTests):
    def test__given_no_existing_questions_in_db__when_get_all__then_empty_list_is_returned(
        self,
    ) -> None:
        # When
        questions = ORMQuestionRepository().get_all()

        # Then
        self.assertEqual(len(questions), 0)

    def test__given_a_question__when_get_all__then_question_information_is_returned(
        self,
    ) -> None:
        # Given
        event = self.given_event_in_orm(
            new_id=uuid.UUID("ef6f6fb3-ba46-43dd-a0da-95de8125b1cc"), name="event"
        )
        question = Question(
            id=uuid.UUID("ef6f6fb3-ba12-43dd-a0da-95de8125b1cc"),
            question="question",
            question_type=QuestionType.TEXT,
            options="",
            event=event,
            created_at=datetime.now(tz=timezone.utc),
            updated_at=datetime.now(tz=timezone.utc),
        )
        ORMQuestionRepository().create(question=question)

        # When
        questions = ORMQuestionRepository().get_all()

        # Then
        self.assertEqual(len(questions), 1)
