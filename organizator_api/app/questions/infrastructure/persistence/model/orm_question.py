from django.db import models

from app.questions.domain.models.question import QuestionType


class ORMQuestion(models.Model):
    class Meta:
        db_table = "question"

    id = models.UUIDField(primary_key=True)
    question = models.TextField()
    question_type = models.CharField(max_length=255, choices=QuestionType.choices())
    options = models.CharField(max_length=255, null=True)
    event = models.ForeignKey("ORMEvent", on_delete=models.CASCADE)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
