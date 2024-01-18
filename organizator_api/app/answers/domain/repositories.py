import uuid
from abc import ABC, abstractmethod
from typing import List

from app.answers.domain.models.answer import Answer


class AnswersRepository(ABC):
    @abstractmethod
    def create(self, answer: Answer) -> None:
        pass

    @abstractmethod
    def get_by_application_id(self, application_id: uuid.UUID) -> List[Answer]:
        pass
