import uuid
from typing import List

from app.questions.domain.exceptions import QuestionDoesNotExist
from app.questions.domain.models.question import Question
from app.questions.domain.repositories import QuestionRepository


class QuestionRepositoryMock(QuestionRepository):
    def __init__(self) -> None:
        self.questions: List[Question] = []

    def create(self, question: Question) -> None:
        self.questions.append(question)

    def update(self, question: Question) -> None:
        for q in self.questions:
            if q.id == question.id:
                q.question = question.question
                q.question_type = question.question_type
                q.options = question.options
                q.updated_at = question.updated_at
                return
        raise QuestionDoesNotExist()

    def get_by_event_id(self, event_id: uuid.UUID) -> List[Question]:
        list = []
        for question in self.questions:
            if question.event.id == event_id:
                list.append(question)

        return list

    def get(self, question_id: uuid.UUID) -> Question:
        for question in self.questions:
            if question.id == question_id:
                return question
        raise QuestionDoesNotExist()

    def get_all(self) -> List[Question]:
        return self.questions

    def clear(self) -> None:
        self.questions = []
