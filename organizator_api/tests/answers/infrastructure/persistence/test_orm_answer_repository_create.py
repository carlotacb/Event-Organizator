import uuid
from datetime import datetime, timezone

from app.answers.domain.exceptions import AnswerAlreadyExists
from app.answers.domain.models.answer import Answer
from app.answers.infrastructure.persistence.model.orm_answers import ORMAnswers
from app.answers.infrastructure.persistence.orm_answers_respository import (
    ORMAnswersRepository,
)
from tests.api_tests import ApiTests


class TestORMAnswerRepositoryCreate(ApiTests):
    def test__given_a_answer_with_a_valid_question_and_user__when_create__then_answer_is_saved(
        self,
    ) -> None:
        # Given
        application = self.given_application_in_orm(
            new_id=uuid.UUID("ef6f6fb3-ba46-43dd-a0da-95de8125b1cc")
        )
        question = self.given_question_in_orm(
            new_id=uuid.UUID("ef6f6fb3-ba46-43dd-a0da-95de8125b1cc")
        )

        answer = Answer(
            id=uuid.UUID("ef6f6fb3-ba12-43dd-a0da-95de8125b1cc"),
            answer="answer",
            question=question,
            application=application,
            created_at=datetime.now(tz=timezone.utc),
            updated_at=datetime.now(tz=timezone.utc),
        )

        # When
        ORMAnswersRepository().create(answer=answer)

        # Then
        self.assertIsNotNone(ORMAnswers.objects.get(id=str(answer.id)))

    def test__given_a_application_already_created__when_create__then_answer_already_exists_is_raised(
        self,
    ) -> None:
        # Given
        application = self.given_application_in_orm(
            new_id=uuid.UUID("ef6f6fb3-ba46-43dd-a0da-95de8125b1cc")
        )
        question = self.given_question_in_orm(
            new_id=uuid.UUID("ef6f6fb3-ba46-43dd-a0da-95de8125b1cc")
        )

        answer = Answer(
            id=uuid.UUID("ef6f6fb3-ba12-43dd-a0da-95de8125b1cc"),
            answer="answer",
            question=question,
            application=application,
            created_at=datetime.now(tz=timezone.utc),
            updated_at=datetime.now(tz=timezone.utc),
        )

        ORMAnswersRepository().create(answer=answer)

        answer2 = Answer(
            id=uuid.UUID("ef6f6fb3-ba12-49dd-a0da-95de8125b4cc"),
            answer="new answer",
            question=question,
            application=application,
            created_at=datetime.now(tz=timezone.utc),
            updated_at=datetime.now(tz=timezone.utc),
        )

        # When / Then
        with self.assertRaises(AnswerAlreadyExists):
            ORMAnswersRepository().create(answer=answer2)
