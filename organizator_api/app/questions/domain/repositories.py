import uuid
from abc import ABC, abstractmethod
from typing import List

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

    @abstractmethod
    def get_by_event_id(self, event_id: uuid.UUID) -> List[Question]:
        pass

    @abstractmethod
    def get_all(self) -> List[Question]:
        pass
