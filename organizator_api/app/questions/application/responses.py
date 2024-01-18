from dataclasses import dataclass
from typing import Any

from app.questions.domain.models.question import Question


@dataclass
class QuestionResponse:
    id: str
    question: str
    question_type: str
    options: str

    @staticmethod
    def from_question(question: Question) -> "QuestionResponse":
        return QuestionResponse(
            id=str(question.id),
            question=question.question,
            question_type=question.question_type.value,
            options=question.options,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "question": self.question,
            "question_type": self.question_type,
            "options": self.options,
        }
