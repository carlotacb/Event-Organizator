import uuid
from datetime import datetime, timezone

from app.users.infrastructure.repository_factories import UserRepositoryFactory
from app.users.application.requests import UpdateUserRequest
from app.users.domain.models.user import User


class UpdateUserUseCase:
    def __init__(self) -> None:
        self.user_repository = UserRepositoryFactory.create()

    def execute(self, user_id: uuid.UUID, user: UpdateUserRequest) -> User:
        original_user = self.user_repository.get_by_id(user_id)
        new_user = User(
            id=user_id,
            email=original_user.email,
            password=original_user.password,
            username=user.username if user.username else original_user.username,
            profile_image=user.profile_image
            if user.profile_image
            else original_user.profile_image,
            first_name=user.first_name if user.first_name else original_user.first_name,
            last_name=user.last_name if user.last_name else original_user.last_name,
            bio=user.bio if user.bio else original_user.bio,
            created_at=original_user.created_at,
            updated_at=datetime.now(tz=timezone.utc),
        )

        self.user_repository.update(new_user)
        return new_user
