from django.test import TestCase

from app.questions.domain.repositories import QuestionRepository
from app.questions.infrastructure.repository_factories import QuestionRepositoryFactory


class TestRepositoryFactories(TestCase):
    def test__given_event_repository_factory__when_create__then_returns_event_repository(
        self,
    ) -> None:
        repository = QuestionRepositoryFactory.create()
        assert isinstance(repository, QuestionRepository)
