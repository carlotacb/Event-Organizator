import uuid

from app.questions.application.request import UpdateQuestionRequest
from app.questions.domain.models.question import QuestionType
from app.questions.domain.usecases.update_question_use_case import UpdateQuestionUseCase
from app.users.domain.exceptions import OnlyAuthorizedToOrganizerAdmin
from app.users.domain.models.user import UserRoles
from tests.api_tests import ApiTests
from tests.events.domain.EventFactory import EventFactory
from tests.questions.domain.QuestionFactory import QuestionFactory
from tests.users.domain.UserFactory import UserFactory


class TestUpdateQuestionUseCase(ApiTests):
    def setUp(self) -> None:
        super().setUp()
        self.event_repository.clear()
        self.question_repository.clear()

        self.event_id = uuid.UUID("eb41b762-5988-4fa3-8942-7a91ccb00686")
        event = EventFactory().create(new_id=self.event_id)
        self.event_repository.create(event)

        self.question_id = uuid.UUID("eb41b762-5988-4fa3-8942-7a91ccb00686")
        question = QuestionFactory().create(
            new_id=self.question_id,
            event=event,
        )
        self.question_repository.create(question)

    def test__given_a_non_organizer_user__when_update_use_case__then_only_authorized_to_organizers_is_raised(
        self,
    ) -> None:
        # Given
        token = uuid.UUID("eb41b762-5988-4fa3-8942-7a91ccb00686")
        user_complete = UserFactory().create(
            token=token,
            role=UserRoles.PARTICIPANT,
        )
        self.user_repository.create(user_complete)
        question_data = UpdateQuestionRequest(
            question="Question",
            question_type="TEXT",
            options="",
        )

        # When / Then
        with self.assertRaises(OnlyAuthorizedToOrganizerAdmin):
            UpdateQuestionUseCase().execute(
                question_id=self.question_id,
                question_data=question_data,
                token=token,
            )

    def test__given_a_organizer_user__when_update_use_case__then_question_is_updated(
        self,
    ) -> None:
        # Given
        token = uuid.UUID("eb41b762-5988-4fa3-8942-7a91ccb00686")
        user_complete = UserFactory().create(
            token=token,
            role=UserRoles.ORGANIZER_ADMIN,
        )
        self.user_repository.create(user_complete)
        question_data = UpdateQuestionRequest(
            question="Question is updated",
        )

        # When
        UpdateQuestionUseCase().execute(
            question_id=self.question_id,
            question_data=question_data,
            token=token,
        )

        # Then
        question = self.question_repository.get(self.question_id)
        self.assertEqual(question.question, "Question is updated")
        self.assertEqual(question.question_type, QuestionType.TEXT)
        self.assertEqual(question.options, "")
