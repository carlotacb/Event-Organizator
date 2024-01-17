import uuid

from app.events.domain.exceptions import EventNotFound
from app.questions.application.request import CreateQuestionRequest
from app.questions.domain.models.question import QuestionType
from app.questions.domain.usecases.create_new_question_use_case import (
    CreateNewQuestionUseCase,
)
from app.users.domain.exceptions import OnlyAuthorizedToOrganizerAdmin
from app.users.domain.models.user import UserRoles, TShirtSizes, GenderOptions
from tests.api_tests import ApiTests
from tests.events.domain.EventFactory import EventFactory
from tests.users.domain.UserFactory import UserFactory


class TestCreateNewQuestionUseCase(ApiTests):
    def setUp(self) -> None:
        super().setUp()
        self.event_repository.clear()
        self.question_repository.clear()

        self.event_id = uuid.UUID("eb41b762-5988-4fa3-8942-7a91ccb00686")
        event = EventFactory().create(new_id=self.event_id)
        self.event_repository.create(event)

    def test__given_a_non_existing_event__when_create_question__then_event_not_found_is_raised(
        self,
    ) -> None:
        # Given
        question_data = CreateQuestionRequest(
            event_id=uuid.uuid4(),
            question="Question",
            question_type="TEXT",
            options="None",
        )

        # When / Then
        with self.assertRaises(EventNotFound):
            CreateNewQuestionUseCase().execute(
                token=uuid.uuid4(), question_data=question_data
            )

    def test__given_correct_question_data_and_a_participant_user_token__when_create_application__then_only_authorized_to_organizers_is_raised(
        self,
    ) -> None:
        # Given
        token = uuid.UUID("eb41b762-5988-4fa3-8942-7a91ccb00686")
        user_complete = UserFactory().create(
            token=token,
            role=UserRoles.PARTICIPANT,
            new_id=uuid.UUID("eb41b762-5988-4fa3-8942-7a91ccb00686"),
            tshirt=TShirtSizes.M,
            gender=GenderOptions.FEMALE,
            alimentary_restrictions="No restrictions",
            email="email@test.com",
            username="username",
        )
        self.user_repository.create(user_complete)

        question_data = CreateQuestionRequest(
            event_id=self.event_id,
            question="Question",
            question_type="TEXT",
            options="None",
        )

        # When / Then
        with self.assertRaises(OnlyAuthorizedToOrganizerAdmin):
            CreateNewQuestionUseCase().execute(token=token, question_data=question_data)

    def test__given_correct_question_data_and_a_organizer_user_token__when_create_application__then_question_is_created(
        self,
    ) -> None:
        # Given
        token = uuid.UUID("eb41b762-5988-4fa3-8942-7a91ccb00686")
        user_complete = UserFactory().create(
            token=token,
            role=UserRoles.ORGANIZER_ADMIN,
            new_id=uuid.UUID("eb41b762-5988-4fa3-8942-7a91ccb00686"),
            tshirt=TShirtSizes.M,
            gender=GenderOptions.FEMALE,
            alimentary_restrictions="No restrictions",
        )
        self.user_repository.create(user_complete)

        question_data = CreateQuestionRequest(
            event_id=self.event_id,
            question="Question",
            question_type="TEXT",
            options="None",
        )

        # When
        CreateNewQuestionUseCase().execute(token=token, question_data=question_data)

        # Then
        questions = self.question_repository.get_all()
        self.assertEqual(len(questions), 1)
        self.assertEqual(questions[0].question, "Question")
        self.assertEqual(questions[0].question_type, QuestionType.TEXT)
        self.assertEqual(questions[0].options, "None")
        self.assertEqual(questions[0].event.id, self.event_id)
        self.assertIsNotNone(questions[0].created_at)
        self.assertIsNotNone(questions[0].updated_at)
