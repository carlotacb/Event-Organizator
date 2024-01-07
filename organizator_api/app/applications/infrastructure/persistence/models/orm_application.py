from django.db import models

from app.events.infrastructure.persistence.models.orm_event import ORMEvent
from app.users.infrastructure.persistence.models.orm_user import ORMUser


class ORMApplication(models.Model):
    class Meta:
        db_table = "application"

    id = models.UUIDField(primary_key=True)
    user_id = models.ForeignKey(ORMUser, on_delete=models.CASCADE)
    event_id = models.ForeignKey(ORMEvent, on_delete=models.CASCADE)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    options = models.CharField(max_length=255, null=True, default=None)