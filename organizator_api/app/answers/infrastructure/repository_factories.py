from app.answers.domain.repositories import AnswersRepository
from app.answers.infrastructure.persistence.orm_answers_respository import (
    ORMAnswersRepository,
)


class AnswerRepositoryFactory:
    _answers_repository = None

    @staticmethod
    def create() -> AnswersRepository:
        if AnswerRepositoryFactory._answers_repository is None:
            AnswerRepositoryFactory._answers_repository = ORMAnswersRepository()

        return AnswerRepositoryFactory._answers_repository
