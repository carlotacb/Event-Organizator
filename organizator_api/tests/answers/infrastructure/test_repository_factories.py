from django.test import TestCase

from app.answers.domain.repositories import AnswersRepository
from app.answers.infrastructure.repository_factories import AnswerRepositoryFactory


class TestRepositoryFactories(TestCase):
    def test__given_answer_repository_factory__when_create__then_returns_answer_repository(
        self,
    ):
        repository = AnswerRepositoryFactory.create()
        assert isinstance(repository, AnswersRepository)
