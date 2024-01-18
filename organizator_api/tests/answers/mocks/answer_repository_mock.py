import uuid
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

    def get_by_application_id(self, application_id: uuid.UUID) -> List[Answer]:
        list = []
        for answer in self.answer:
            if answer.application.id == application_id:
                list.append(answer)

        return list

    def clear(self) -> None:
        self.answer = []
