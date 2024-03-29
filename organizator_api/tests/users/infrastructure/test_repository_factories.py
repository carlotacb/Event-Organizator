from django.test import TestCase

from app.users.domain.repositories import UserRepository
from app.users.infrastructure.repository_factories import UserRepositoryFactory


class TestRepositoryFactories(TestCase):
    def test__given_event_repository_factory__when_create__then_returns_event_repository(
        self,
    ) -> None:
        repository = UserRepositoryFactory.create()
        assert isinstance(repository, UserRepository)
