from django.db import models


class ORMAnswers(models.Model):
    class Meta:
        db_table = "answer"
        unique_together = ["question", "application"]

    id = models.UUIDField(primary_key=True)
    answer = models.TextField()
    question = models.ForeignKey("ORMQuestion", on_delete=models.CASCADE)
    application = models.ForeignKey("ORMEventApplication", on_delete=models.CASCADE)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
