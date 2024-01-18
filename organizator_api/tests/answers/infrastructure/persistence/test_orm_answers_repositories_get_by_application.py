import uuid
from datetime import datetime, timezone

from app.answers.domain.models.answer import Answer
from app.answers.infrastructure.persistence.orm_answers_respository import ORMAnswersRepository
from tests.api_tests import ApiTests


class TestORMAnswersRepositoriesGetByApplication(ApiTests):
    def test__given_answers_in_one_application_for_a_application__when_get_by_application__then_it_returns_the_list(
        self,
    ) -> None:
        # Given
        application_id = uuid.UUID("ef6f6fb3-ba46-43dd-a0da-95de8125b1cc")
        application = self.given_application_in_orm(
            new_id=application_id
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

        # When
        actual_answers = ORMAnswersRepository().get_by_application_id(application_id)

        # Then
        self.assertEqual(len(actual_answers), 1)
