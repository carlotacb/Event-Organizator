import uuid
from abc import ABC, abstractmethod

from app.questions.domain.models.question import Question


class QuestionRepository(ABC):
    @abstractmethod
    def create(self, question: Question) -> None:
        pass

    @abstractmethod
    def update(self, question: Question) -> None:
        pass

    @abstractmethod
    def get(self, question_id: uuid.UUID) -> Question:
        pass
