from app.users.domain.repositories import UserRepository
from app.users.infrastructure.persistance.orm_user_repository import ORMUserRepository


class UserRepositoryFactory:
    _user_repository = None

    @staticmethod
    def create() -> UserRepository:
        if UserRepositoryFactory._user_repository is None:
            UserRepositoryFactory._user_repository = ORMUserRepository()

        return UserRepositoryFactory._user_repository
