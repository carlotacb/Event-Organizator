import uuid
from datetime import datetime, timezone

from app.questions.domain.models.question import Question, QuestionType
from app.questions.infrastructure.persistence.orm_questions_repository import (
    ORMQuestionRepository,
)
from tests.api_tests import ApiTests


class TestORMQuestionRepositoryGetByEvent(ApiTests):
    def test__given_no_existing_questions_in_db__when_get_by_event__then_empty_list_is_returned(
        self,
    ) -> None:
        # When
        questions = ORMQuestionRepository().get_by_event_id(event_id=uuid.uuid4())

        # Then
        self.assertEqual(len(questions), 0)

    def test__given_some_questions_in_db__when_get_by_event__then_question_information_of_the_event_is_returned(
        self,
    ) -> None:
        # Given
        event = self.given_event_in_orm(
            new_id=uuid.UUID("ef6f6fb3-ba46-43dd-a0da-95de8125b1cc"), name="event"
        )
        event2 = self.given_event_in_orm(
            new_id=uuid.UUID("ef6f6fb3-ba46-43dd-a0da-95de8125b1cd"), name="event2"
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

        question2 = Question(
            id=uuid.UUID("ef6f6fb3-ba12-43dd-a0da-95de8125b2cc"),
            question="question2",
            question_type=QuestionType.TEXT,
            options="",
            event=event2,
            created_at=datetime.now(tz=timezone.utc),
            updated_at=datetime.now(tz=timezone.utc),
        )
        ORMQuestionRepository().create(question=question2)

        question3 = Question(
            id=uuid.UUID("ef6f6fb3-ba12-43dd-a0da-95de8125b3cc"),
            question="question3",
            question_type=QuestionType.TEXT,
            options="",
            event=event,
            created_at=datetime.now(tz=timezone.utc),
            updated_at=datetime.now(tz=timezone.utc),
        )
        ORMQuestionRepository().create(question=question3)

        # When
        questions = ORMQuestionRepository().get_by_event_id(event_id=event.id)

        # Then
        self.assertEqual(len(questions), 2)
