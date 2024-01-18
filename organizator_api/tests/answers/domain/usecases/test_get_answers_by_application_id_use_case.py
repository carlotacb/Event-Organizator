import uuid

from app.answers.domain.exceptions import UserIsNotAuthorOfAnswer
from app.answers.domain.usecases.get_answers_by_application_id_use_case import (
    GetAnswersByApplicationIdUseCase,
)
from tests.answers.domain.AnswerFactory import AnswerFactory
from tests.api_tests import ApiTests
from tests.applications.domain.ApplicationFactory import ApplicationFactory
from tests.events.domain.EventFactory import EventFactory
from tests.questions.domain.QuestionFactory import QuestionFactory
from tests.users.domain.UserFactory import UserFactory


class TestGetAnswersByApplicationIdUseCase(ApiTests):
    def setUp(self) -> None:
        super().setUp()
        self.application_repository.clear()
        self.user_repository.clear()
        self.event_repository.clear()
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

        self.user_participant2 = UserFactory().create(
            new_id=uuid.UUID("eb41b762-5988-4fa3-8949-7a91ccb00686"),
            token=uuid.UUID("eb41b762-5988-4fa3-8949-7a91ccb00686"),
        )
        self.user_repository.create(self.user_participant2)

        self.event_id = uuid.UUID("eb41b762-5988-4fa3-8942-7a91ccb00686")
        self.event = EventFactory().create(new_id=self.event_id, name="HackUPC 2024")
        self.event_repository.create(self.event)

        application = ApplicationFactory().create(
            new_id=uuid.UUID("eb41b762-5988-4fa3-8942-7a91ccb00686"),
            user=self.user_participant,
            event=self.event,
        )
        self.application_repository.create(application)

        self.question = QuestionFactory().create(
            new_id=uuid.UUID("eb41b762-5988-4fa3-8942-7a91ccb00686"),
            event=self.event,
        )
        self.question_repository.create(self.question)

        answer = AnswerFactory().create(
            new_id=uuid.UUID("eb41b762-5988-4fa3-8942-7a91ccb00686"),
            application=application,
            question=self.question,
            answer="answer",
        )
        self.answer_repository.create(answer)

    def test__given_a_user_and_an_application_in_db__when_get_answers_by_application_id__then_returns_the_answers(
        self,
    ) -> None:
        # Given
        application = self.application_repository.get(
            uuid.UUID("eb41b762-5988-4fa3-8942-7a91ccb00686")
        )
        # When
        answers = GetAnswersByApplicationIdUseCase().execute(
            application_id=application.id, token=self.user_token_participant
        )
        # Then
        self.assertEqual(len(answers), 1)

    def test__given_a_user_and_a_application_from_another_user__when_get_answers_by_application_id__then_user_is_not_author_of_answer(
        self,
    ) -> None:
        # When
        with self.assertRaises(UserIsNotAuthorOfAnswer):
            GetAnswersByApplicationIdUseCase().execute(
                application_id=uuid.UUID("eb41b762-5988-4fa3-8942-7a91ccb00686"),
                token=uuid.UUID("eb41b762-5988-4fa3-8949-7a91ccb00686"),
            )
