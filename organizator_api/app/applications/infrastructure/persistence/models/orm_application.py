from django.db import models

from app.applications.domain.models.application import ApplicationStatus


class ORMEventApplication(models.Model):
    class Meta:
        db_table = "event_application"
        unique_together = ["user", "event"]

    id = models.UUIDField(primary_key=True)
    user = models.ForeignKey("ORMUser", on_delete=models.CASCADE)
    event = models.ForeignKey("ORMEvent", on_delete=models.CASCADE)
    status = models.CharField(max_length=255, choices=ApplicationStatus.choices(), default=ApplicationStatus.PENDING.name)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
