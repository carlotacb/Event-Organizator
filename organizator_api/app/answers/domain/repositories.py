from abc import ABC, abstractmethod

from app.answers.domain.models.answer import Answer


class AnswersRepository(ABC):
    @abstractmethod
    def create(self, answer: Answer) -> None:
        pass
