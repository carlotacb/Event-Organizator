import uuid
from datetime import datetime

from app.applications.domain.exceptions import (
    ProfileNotComplete,
    ApplicationAlreadyExists,
    UserIsNotAParticipant,
    UserIsTooYoung,
)
from app.applications.domain.usecases.create_new_application_use_case import (
    CreateNewApplicationUseCase,
)
from app.events.domain.exceptions import EventNotFound
from app.users.domain.exceptions import UserNotFound
from app.users.domain.models.user import UserRoles, TShirtSizes, GenderOptions
from tests.api_tests import ApiTests
from tests.events.domain.EventFactory import EventFactory
from tests.users.domain.UserFactory import UserFactory


class TestCreateNewApplicationUseCase(ApiTests):
    def setUp(self) -> None:
        super().setUp()
        self.application_repository.clear()
        self.user_repository.clear()
        self.event_repository.clear()
        self.user_complete_token = uuid.UUID("ebd8a0f2-eeba-4ddc-b4b9-ab5592ad8e75")
        user_complete = UserFactory().create(
            token=self.user_complete_token,
            role=UserRoles.ORGANIZER,
            new_id=uuid.UUID("eb41b762-5988-4fa3-8942-7a91ccb00686"),
            tshirt=TShirtSizes.M,
            gender=GenderOptions.FEMALE,
            alimentary_restrictions="No restrictions",
            email="email@test.com",
            username="username",
        )
        self.user_repository.create(user_complete)

        self.event_id = uuid.UUID("eb41b762-5988-4fa3-8942-7a91ccb00686")
        event = EventFactory().create(new_id=self.event_id)
        self.event_repository.create(event)

    def test__given_a_user_with_all_the_information_and_non_existing_event__when_create_application__then_event_not_found_is_raised(
        self,
    ) -> None:
        # When / Then
        with self.assertRaises(EventNotFound):
            CreateNewApplicationUseCase().execute(
                token=self.user_complete_token, event_id=uuid.uuid4()
            )

    def test__given_non_existing_user_id_and_existing_event__when_create_application__then_user_not_found_is_raised(
        self,
    ) -> None:
        # When / Then
        with self.assertRaises(UserNotFound):
            CreateNewApplicationUseCase().execute(
                token=uuid.uuid4(), event_id=self.event_id
            )

    def test__given_a_user_without_some_information__when_create_application__then_profile_not_complete_is_raised(
        self,
    ) -> None:
        # Given
        user_token = uuid.UUID("eb41b762-5988-4fa3-8942-7a91ccb00686")
        user = UserFactory().create(token=user_token)
        self.user_repository.create(user)

        # When / Then
        with self.assertRaises(ProfileNotComplete):
            CreateNewApplicationUseCase().execute(
                token=user_token, event_id=self.event_id
            )

    def test__given_a_user_organizer__when_create_application__then_user_is_not_participant(
        self,
    ) -> None:
        # Given
        user_token = uuid.UUID("eb41b762-5988-4fa3-8942-7a91ccb00686")
        user = UserFactory().create(
            token=user_token,
            role=UserRoles.ORGANIZER,
            tshirt=TShirtSizes.M,
            gender=GenderOptions.FEMALE,
            alimentary_restrictions="No restrictions",
        )
        self.user_repository.create(user)

        # When / Then
        with self.assertRaises(UserIsNotAParticipant):
            CreateNewApplicationUseCase().execute(
                token=user_token, event_id=self.event_id
            )

    def test__given_a_user_that_is_14_years_old_and_a_event_with_16_year_old_restriction__when_create_application__then_user_is_too_young_is_returned(
        self,
    ) -> None:
        # Given
        user_token = uuid.UUID("eb41b762-5988-4fa3-8942-7a91ccb00686")
        user = UserFactory().create(
            token=user_token,
            role=UserRoles.PARTICIPANT,
            tshirt=TShirtSizes.M,
            gender=GenderOptions.FEMALE,
            alimentary_restrictions="No restrictions",
            date_of_birth=datetime(2010, 1, 10),
        )
        self.user_repository.create(user)

        # When / Then
        with self.assertRaises(UserIsTooYoung):
            CreateNewApplicationUseCase().execute(
                token=user_token, event_id=self.event_id
            )

    def test__given_a_user_with_all_the_information_and_a_existing_event__when_create_application_two_times_with_the_same_information__then_application_already_exists_is_raised(
        self,
    ) -> None:
        # When / Then
        CreateNewApplicationUseCase().execute(
            token=self.user_complete_token, event_id=self.event_id
        )

        with self.assertRaises(ApplicationAlreadyExists):
            CreateNewApplicationUseCase().execute(
                token=self.user_complete_token, event_id=self.event_id
            )

    def test__given_user_with_all_the_information_and_existing_event__when_create_application__then_the_application_is_created(
        self,
    ) -> None:
        # When
        CreateNewApplicationUseCase().execute(
            token=self.user_complete_token, event_id=self.event_id
        )

        # Then
        applications = self.application_repository.get_all()
        self.assertEqual(len(applications), 1)
