import uuid
from datetime import datetime, timezone

from app.events.domain.exceptions import MissingStudyInformationToCreateUser, MissingWorkInformationToCreateUser
from app.users.application.requests import UpdateUserRequest
from app.users.domain.models.user import User, UserRoles, TShirtSizes, GenderOptions
from app.users.infrastructure.repository_factories import UserRepositoryFactory


class UpdateUserUseCase:
    def __init__(self) -> None:
        self.user_repository = UserRepositoryFactory.create()

    def execute(self, token: uuid.UUID, user_data: UpdateUserRequest) -> User:
        original_user = self.user_repository.get_by_token(token)

        if user_data.work and user_data.current_job_role is None:
            raise MissingWorkInformationToCreateUser

        if user_data.study and (user_data.university is None or user_data.degree is None or user_data.expected_graduation is None):
            raise MissingStudyInformationToCreateUser

        new_user = User(
            id=original_user.id,
            email=original_user.email,
            password=original_user.password,
            first_name=user_data.first_name if user_data.first_name else original_user.first_name,
            last_name=user_data.last_name if user_data.last_name else original_user.last_name,
            username=user_data.username.lower() if user_data.username else original_user.username,
            bio=user_data.bio if user_data.bio else original_user.bio,
            profile_image=user_data.profile_image
            if user_data.profile_image
            else original_user.profile_image,
            date_of_birth=datetime.strptime(user_data.date_of_birth, "%d/%m/%Y") if user_data.date_of_birth else original_user.date_of_birth,
            study=user_data.study if user_data.study else original_user.study,
            work=user_data.work if user_data.work else original_user.work,
            university=user_data.university if user_data.university else original_user.university,
            degree=user_data.degree if user_data.degree else original_user.degree,
            expected_graduation=datetime.strptime(user_data.date_of_birth, "%d/%m/%Y") if user_data.expected_graduation else original_user.expected_graduation,
            current_job_role=user_data.current_job_role if user_data.current_job_role else original_user.current_job_role,
            tshirt=TShirtSizes[user_data.tshirt] if user_data.tshirt else original_user.tshirt,
            gender=GenderOptions[user_data.gender] if user_data.gender else original_user.gender,
            alimentary_restrictions=user_data.alimentary_restrictions if user_data.alimentary_restrictions else original_user.alimentary_restrictions,
            github=user_data.github if user_data.github else original_user.github,
            linkedin=user_data.linkedin if user_data.linkedin else original_user.linkedin,
            devpost=user_data.devpost if user_data.devpost else original_user.devpost,
            webpage=user_data.webpage if user_data.webpage else original_user.webpage,
            created_at=original_user.created_at,
            updated_at=datetime.now(tz=timezone.utc),
            token=original_user.token,
            role=original_user.role,
        )

        self.user_repository.update(new_user)
        return new_user
