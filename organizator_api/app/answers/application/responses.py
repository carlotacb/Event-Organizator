from dataclasses import dataclass
from typing import Any

from app.answers.domain.models.answer import Answer


@dataclass
class AnswerResponse:
    id: str
    question_id: str
    question: str
    answer: str

    @staticmethod
    def from_answer(answer: Answer) -> "AnswerResponse":
        return AnswerResponse(
            id=str(answer.id),
            question_id=str(answer.question.id),
            question=answer.question.question,
            answer=answer.answer,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "question_id": self.question_id,
            "question": self.question,
            "answer": self.answer,
        }
