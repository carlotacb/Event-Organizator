from tests.api_tests import ApiTests
from app.users.application.requests import CreateUserRequest
from app.users.domain.use_cases.create_user_use_case import CreateUserUseCase


class TestCreateUserUseCase(ApiTests):
    def setUp(self) -> None:
        super().setUp()
        self.user_repository.clear()

    def test__given_create_user_request__when_create_user__then_the_user_is_created(
        self,
    ) -> None:
        # Given
        user_data = CreateUserRequest(
            email="carlota@hackupc.com",
            password="1234",
            first_name="Carlota",
            last_name="Catot",
            username="carlota",
            bio="I'm a cat",
            profile_image="https://www.hacknights.dev/images/hacknight.png",
        )

        # When
        CreateUserUseCase().execute(user_data)

        # Then
        users = self.user_repository.get_all()
        self.assertEqual(len(users), 1)