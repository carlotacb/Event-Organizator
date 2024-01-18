import uuid

from app.questions.domain.models.question import Question
from app.questions.infrastructure.repository_factories import QuestionRepositoryFactory


class GetQuestionsByIdUseCase:
    def __init__(self) -> None:
        self.question_repository = QuestionRepositoryFactory.create()

    def execute(self, question_id: uuid.UUID) -> Question:
        return self.question_repository.get(question_id)
