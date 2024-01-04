import uuid

from app.users.domain.exceptions import OnlyAuthorizedToOrganizerAdmin
from app.users.domain.models.user import UserRoles
from app.users.domain.usecases.update_user_role_use_case import UpdateUserRoleUseCase
from tests.api_tests import ApiTests
from tests.users.domain.UserFactory import UserFactory


class TestUpdateRoleUseCase(ApiTests):
    def setUp(self) -> None:
        super().setUp()
        self.user_repository.clear()

        self.user_token = uuid.UUID("5b90906e-2894-467d-835e-3e4fbe42af9f")
        user = UserFactory().create(
            token=self.user_token, role=UserRoles.ORGANIZER_ADMIN
        )
        self.user_repository.create(user)

        self.user_token2 = uuid.UUID("5b90906e-2894-467d-835e-3e4fbe42af9e")
        user2 = UserFactory().create(
            token=self.user_token2,
            email="carlota2@hackupc.com",
            username="charlie",
            new_id=uuid.UUID("17b3d2d2-cbbd-4e37-ad68-756967fd31fe"),
        )
        self.user_repository.create(user2)

    def test__given_user_in_db_participant_and_another_organizer_admin__when_update_user_role__then_the_user_role_is_updated(
        self,
    ) -> None:
        # When
        user = UpdateUserRoleUseCase().execute(
            token=self.user_token,
            user_id=uuid.UUID("17b3d2d2-cbbd-4e37-ad68-756967fd31fe"),
            new_role=UserRoles.ORGANIZER.name,
        )

        # Then
        self.assertEqual(UserRoles.ORGANIZER, user.role)

    def test__given_user_in_db_participant__when_update_user_role_to_organizer__then_it_raises_exception(
        self,
    ) -> None:
        with self.assertRaises(OnlyAuthorizedToOrganizerAdmin):
            UpdateUserRoleUseCase().execute(
                token=self.user_token2,
                user_id=uuid.UUID("17b3d2d2-cbbd-4e37-ad68-756967fd31fe"),
                new_role=UserRoles.ORGANIZER.name,
            )
