from app.questions.domain.repositories import QuestionRepository
from app.questions.infrastructure.persistence.orm_questions_repository import (
    ORMQuestionRepository,
)


class QuestionRepositoryFactory:
    _questions_repository = None

    @staticmethod
    def create() -> QuestionRepository:
        if QuestionRepositoryFactory._questions_repository is None:
            QuestionRepositoryFactory._questions_repository = ORMQuestionRepository()

        return QuestionRepositoryFactory._questions_repository
