from typing import List

from app.questions.domain.exceptions import QuestionAlreadyExists
from app.questions.domain.models.question import Question
from app.questions.domain.repositories import QuestionRepository


class QuestionRepositoryMock(QuestionRepository):
    def __init__(self) -> None:
        self.questions: List[Question] = []

    def create(self, question: Question) -> None:
        for q in self.questions:
            if question.id == q.id:
                raise QuestionAlreadyExists

        self.questions.append(question)

    def get_all(self) -> List[Question]:
        return self.questions

    def clear(self) -> None:
        self.questions = []
