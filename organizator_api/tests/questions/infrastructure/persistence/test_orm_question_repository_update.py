import uuid
from datetime import datetime, timezone

from app.questions.domain.exceptions import QuestionDoesNotExist
from app.questions.domain.models.question import QuestionType, Question
from app.questions.infrastructure.persistence.model.orm_question import ORMQuestion
from app.questions.infrastructure.persistence.orm_questions_repository import (
    ORMQuestionRepository,
)
from tests.api_tests import ApiTests


class TestORMQuestionRepositoryUpdate(ApiTests):
    def test__given_a_question_with_a_valid_event__when_update__then_question_does_not_exist_is_raised(
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
            ORMQuestionRepository().update(question=question)

    def test__given_a_question_with_valid_event_in_db__when_update__then_the_question_is_updated(
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
        question.question = "question2"
        ORMQuestionRepository().update(question=question)

        # Then
        self.assertEqual(
            ORMQuestion.objects.get(id=str(question.id)).question, "question2"
        )
