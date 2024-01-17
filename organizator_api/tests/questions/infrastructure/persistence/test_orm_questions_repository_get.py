import uuid
from datetime import datetime, timezone

from app.questions.domain.exceptions import QuestionDoesNotExist
from app.questions.domain.models.question import QuestionType, Question
from app.questions.infrastructure.persistence.orm_questions_repository import (
    ORMQuestionRepository,
)
from tests.api_tests import ApiTests


class TestORMQuestionsRepositoryGet(ApiTests):
    def test__given_no_existing_question_in_db__when_get__then_question_does_not_exist_is_raised(
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

        # When
        with self.assertRaises(QuestionDoesNotExist):
            ORMQuestionRepository().get(question_id=question.id)

    def test__given_a_question_id__when_get__then_question_information_is_returned(
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
        question_returned = ORMQuestionRepository().get(question_id=question.id)

        # Then
        self.assertEqual(question_returned.id, question.id)
        self.assertEqual(question_returned.question, question.question)
        self.assertEqual(question_returned.question_type, question.question_type)
        self.assertEqual(question_returned.options, question.options)
        self.assertEqual(question_returned.event.id, question.event.id)
        self.assertEqual(question_returned.created_at, question.created_at)
        self.assertEqual(question_returned.updated_at, question.updated_at)
