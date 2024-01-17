import uuid
from datetime import datetime, timezone

from app.questions.domain.exceptions import QuestionAlreadyExists
from app.questions.domain.models.question import Question, QuestionType
from app.questions.infrastructure.persistence.model.orm_question import ORMQuestion
from app.questions.infrastructure.persistence.orm_questions_repository import (
    ORMQuestionRepository,
)
from tests.api_tests import ApiTests


class TestORMQuestionRepositoryCreate(ApiTests):
    def test__given_a_question_with_a_valid_event__when_create__then_question_is_saved(
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
        ORMQuestionRepository().create(question=question)

        # Then
        self.assertIsNotNone(ORMQuestion.objects.get(id=str(question.id)))

    def test__given_different_questions_for_the_same_event__when_create__then_all_of_them_are_created(
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
        question2 = Question(
            id=uuid.UUID("ef6f6fb3-ba12-43dd-a0da-95de8125b5cc"),
            question="question",
            question_type=QuestionType.TEXT,
            options="",
            event=event,
            created_at=datetime.now(tz=timezone.utc),
            updated_at=datetime.now(tz=timezone.utc),
        )

        # When
        ORMQuestionRepository().create(question=question)
        ORMQuestionRepository().create(question=question2)

        # Then
        self.assertIsNotNone(ORMQuestion.objects.get(id=str(question.id)))
        self.assertIsNotNone(ORMQuestion.objects.get(id=str(question2.id)))
