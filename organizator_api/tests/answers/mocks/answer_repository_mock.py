from typing import List

from app.answers.domain.models.answer import Answer
from app.answers.domain.repositories import AnswersRepository


class AnswerRepositoryMock(AnswersRepository):
    def __init__(self) -> None:
        self.answer: List[Answer] = []

    def create(self, answer: Answer) -> None:
        self.answer.append(answer)

    def get_all(self) -> List[Answer]:
        return self.answer

    def clear(self) -> None:
        self.answer = []
