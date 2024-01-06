import json
import uuid

from tests.api_tests import ApiTests
from tests.users.domain.UserFactory import UserFactory


class TestViewUpdateMyUser(ApiTests):
    def setUp(self) -> None:
        super().setUp()
        self.user_repository.clear()
        self.token = "baad2fe5-0122-459b-9572-625c3351d6ac"
        user = UserFactory().create(token=uuid.UUID(self.token))
        self.user_repository.create(user)
        self.token_worker = "baad2fe5-0122-459b-9572-625c3351d6ad"
        user_worker = UserFactory().create(
            token=uuid.UUID(self.token_worker),
            new_id=uuid.UUID("be0f4c18-4a7c-4c1e-8a62-fc50916b6c88"),
            email="carlota@test.com",
            username="carkbra",
            work=True,
            current_job_role="Software Engineer",
            study=False,
            university=None,
            degree=None,
            expected_graduation=None,
        )
        self.user_repository.create(user_worker)



    def test_given_user_body__when_update_without_header__then_unauthorized_is_returned(
            self,
    ) -> None:
        # Given
        body = {"username": "charlie"}

        # When
        response = self.client.post(
            "/organizator-api/users/update/me",
            json.dumps(body),
            content_type="application/json",
        )

        # Then
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.content, b"Unauthorized")

    def test__given_user_body__when_update_user_with_a_invalid_token__then_error_is_returned(
            self,
    ) -> None:
        # Given
        body = {"username": "charlie"}

        # When
        header = {"HTTP_Authorization": "invalid_token"}
        response = self.client.post(
            "/organizator-api/users/update/me",
            json.dumps(body),
            content_type="application/json",
            **header,  # type: ignore
        )

        # Then
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b"Invalid token")

    def test__given_user_in_db_and_body_with_email__when_update__then_email_cannot_be_updated_is_returned(
            self,
    ) -> None:
        # Given
        body = {"email": "carlota@hackupc.com"}

        # When
        header = {"HTTP_Authorization": self.token}
        response = self.client.post(
            "/organizator-api/users/update/me",
            json.dumps(body),
            content_type="application/json",
            **header,  # type: ignore
        )

        # Then
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.content, b"The email cannot be updated")

    def test__given_user_in_db_and_body_with_password__when_update__then_password_cannot_be_updated_is_returned(
            self,
    ) -> None:
        # Given
        body = {"password": "carlotacb"}

        # When
        header = {"HTTP_Authorization": self.token}
        response = self.client.post(
            "/organizator-api/users/update/me",
            json.dumps(body),
            content_type="application/json",
            **header,  # type: ignore
        )

        # Then
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.content, b"The password cannot be updated")

    def test__given_student_user_in_db_and_body_that_change_to_work__when_update__then_missing_work_information_to_create_user_is_returned(self) -> None:
        # Given
        body = {"work": True}

        # When
        header = {"HTTP_Authorization": self.token}
        response = self.client.post(
            "/organizator-api/users/update/me",
            json.dumps(body),
            content_type="application/json",
            **header,  # type: ignore
        )

        # Then
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.content, b"Missing work information to create user")

    def test__given_worker_user_in_db_and_body_that_change_to_study__when_update__then_missing_study_information_to_create_user_is_returned(self) -> None:
        # Given
        body = {"study": True}

        # When
        header = {"HTTP_Authorization": self.token_worker}
        response = self.client.post(
            "/organizator-api/users/update/me",
            json.dumps(body),
            content_type="application/json",
            **header,  # type: ignore
        )

        # Then
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.content, b"Missing study information to create user")


    def test__given_a_user_body__when_update_with_a_non_existing_token__then_user_does_not_exist_is_returned(
            self,
    ) -> None:
        # Given
        body = { "bio": "I'm Charlie" }

        # When
        header = {"HTTP_Authorization": "baad2fe5-0122-459b-9572-625c3351d7dd"}
        response = self.client.post(
            "/organizator-api/users/update/me",
            json.dumps(body),
            content_type="application/json",
            **header,  # type: ignore
        )

        # Then
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content, b"User does not exist")


    def test__given_body_changing_username_that_already_exists_in_db__when_update_user__then_the_username_you_are_using_is_already_taken_is_returned(
            self,
    ) -> None:
        # Given
        body = {"username": "carkbra"}

        # When
        header = {"HTTP_Authorization": self.token}
        response = self.client.post(
            "/organizator-api/users/update/me",
            json.dumps(body),
            content_type="application/json",
            **header,  # type: ignore
        )

        # Then
        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.content, b"The username you are using is already taken")

    def test__given_user_in_db__when_update_user__then_user_is_updated(self) -> None:
        # Given
        body = {
            "username": "charlie",
            "first_name": "Charlie",
            "last_name": "Brown",
            "bio": "I'm Charlie",
            "profile_image": "https://www.google.com",
        }

        # When
        header = {"HTTP_Authorization": self.token}
        response = self.client.post(
            "/organizator-api/users/update/me",
            json.dumps(body),
            content_type="application/json",
            **header,  # type: ignore
        )

        # Then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.content,
            b'{"id": "ef6f6fb3-ba12-43dd-a0da-95de8125b1cc", "username": "charlie", "email": "carlota@hackupc.com", "first_name": "Charlie", "last_name": "Brown", "bio": "I\'m Charlie", "profile_image": "https://www.google.com", "role": "Participant", "date_of_birth": "07/05/1996", "study": true, "work": false, "university": "Universitat Polit\\u00e8cnica de Catalunya", "degree": "Computer Science", "expected_graduation": "01/05/2024", "current_job_role": "", "tshirt": "", "gender": "", "alimentary_restrictions": "", "github": "", "linkedin": "", "devpost": "", "webpage": ""}',
        )



