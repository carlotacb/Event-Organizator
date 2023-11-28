import uuid

from app.users.application.requests import UpdateUserRequest
from app.users.domain.usecases.update_user_use_case import UpdateUserUseCase
from tests.api_tests import ApiTests
from tests.users.domain.UserFactory import UserFactory


class TestUpdateUserUseCase(ApiTests):
    def setUp(self) -> None:
        super().setUp()
        self.user_repository.clear()
        user = UserFactory().create()
        self.user_repository.create(user)

    def test__given_update_user_request__when_update_user__then_the_user_is_updated(
        self,
    ) -> None:
        # Given
        user_data = UpdateUserRequest(
            username="carlota",
            first_name="Carlota",
            last_name="Catot",
            bio="I'm a cat",
            profile_image="https://www.hacknights.dev/images/hacknight.png",
        )

        # When
        user = UpdateUserUseCase().execute(
            user_id=uuid.UUID("ef6f6fb3-ba12-43dd-a0da-95de8125b1cc"), user=user_data
        )

        # Then
        self.assertEqual("carlota", user.username)
        self.assertEqual("Carlota", user.first_name)
        self.assertEqual("Catot", user.last_name)
        self.assertEqual("I'm a cat", user.bio)
        self.assertEqual(
            "https://www.hacknights.dev/images/hacknight.png", user.profile_image
        )
        self.assertEqual("carlota@hackupc.com", user.email)

    def test__given_update_user_request_with_empty_fields__when_update_user__then_the_user_is_not_updated(
        self,
    ) -> None:
        # Given
        user_data = UpdateUserRequest(
            username="",
            first_name="",
            last_name="",
            bio="",
            profile_image="",
        )

        # When
        user = UpdateUserUseCase().execute(
            user_id=uuid.UUID("ef6f6fb3-ba12-43dd-a0da-95de8125b1cc"), user=user_data
        )

        # Then
        self.assertEqual("carlotacb", user.username)
        self.assertEqual("Carlota", user.first_name)
        self.assertEqual("Catot", user.last_name)
        self.assertEqual("The user that is using this application", user.bio)
        self.assertEqual(
            "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png",
            user.profile_image,
        )

    def test__given_update_user_request_with_only_bio__when_update_user__then_the_user_is_updated(
        self,
    ) -> None:
        # Given
        user_data = UpdateUserRequest(
            bio="I'm the beeest",
        )

        # When
        user = UpdateUserUseCase().execute(
            user_id=uuid.UUID("ef6f6fb3-ba12-43dd-a0da-95de8125b1cc"), user=user_data
        )

        # Then
        self.assertEqual("carlotacb", user.username)
        self.assertEqual("Carlota", user.first_name)
        self.assertEqual("Catot", user.last_name)
        self.assertEqual("I'm the beeest", user.bio)
        self.assertEqual(
            "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png",
            user.profile_image,
        )