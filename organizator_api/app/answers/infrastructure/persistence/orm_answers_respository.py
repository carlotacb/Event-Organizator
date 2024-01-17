from app.answers.domain.exceptions import AnswerDoesNotExist
from app.answers.domain.models.answer import Answer
from app.answers.domain.repositories import AnswersRepository
from app.answers.infrastructure.persistence.model.orm_answers import ORMAnswers
from app.questions.infrastructure.persistence.model.orm_question import ORMQuestion
from app.users.infrastructure.persistence.models.orm_user import ORMUser


class ORMAnswersRepository(AnswersRepository):
    def create(self, answer: Answer) -> None:
        question = ORMQuestion.objects.get(id=answer.question.id)
        user = ORMUser.objects.get(id=answer.id)

        ORMAnswers(
            id=answer.id,
            answer=answer.answer,
            question=question,
            user=user,
            created_at=answer.created_at,
            updated_at=answer.updated_at,
        ).save()
