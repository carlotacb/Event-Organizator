import uuid

from app.events.application.requests import CreateEventRequest
from app.events.domain.usecases.create_event_use_case import CreateEventUseCase
from app.users.domain.exceptions import OnlyAuthorizedToOrganizerAdmin
from app.users.domain.models.user import UserRoles
from tests.api_tests import ApiTests
from tests.users.domain.UserFactory import UserFactory


class TestCreateEventUseCase(ApiTests):
    def setUp(self) -> None:
        super().setUp()
        self.event_repository.clear()
        self.user_repository.clear()

    def test__given_create_event_request__when_create_event__then_the_event_is_created(
        self,
    ) -> None:
        # Given
        user_token = uuid.UUID("5b90906e-2894-467d-835e-3e4fbe42af9f")
        user = UserFactory().create(token=user_token, role=UserRoles.ORGANIZER_ADMIN)
        self.user_repository.create(user)
        event_data = CreateEventRequest(
            name="HackNight Ep.VI",
            url="https://www.hacknights.dev",
            description="The best hack-night ever",
            start_date="17/11/2023 21:00",
            end_date="18/11/2023 05:00",
            location="Aula d'estudis Campus Nord",
            header_image="https://www.hacknights.dev/images/hacknight.png",
            open_for_participants=True,
            max_participants=100,
            expected_attrition_rate=0.1,
            students_only=True,
            age_restrictions=16,
        )

        # When
        CreateEventUseCase().execute(user_token, event_data)

        # Then
        events = self.event_repository.get_all()
        self.assertEqual(len(events), 1)

    def test__given_token_for_creation_that_is_not_admin__when_create_event__then_raise_exception(
        self,
    ) -> None:
        # Given
        user_token = uuid.UUID("ebd8a0f2-eeba-4ddc-b4b9-ab5592ad8e75")
        user = UserFactory().create(
            token=user_token,
            role=UserRoles.ORGANIZER,
            new_id=uuid.UUID("eb41b762-5988-4fa3-8942-7a91ccb00686"),
        )
        self.user_repository.create(user)

        event_data = CreateEventRequest(
            name="HackNight Ep.VI",
            url="https://www.hacknights.dev",
            description="The best hack-night ever",
            start_date="17/11/2023 21:00",
            end_date="18/11/2023 05:00",
            location="Aula d'estudis Campus Nord",
            header_image="https://www.hacknights.dev/images/hacknight.png",
            open_for_participants=True,
            max_participants=100,
            expected_attrition_rate=0.1,
            students_only=True,
            age_restrictions=16
        )

        # When / Then
        with self.assertRaises(OnlyAuthorizedToOrganizerAdmin):
            CreateEventUseCase().execute(user_token, event_data)
