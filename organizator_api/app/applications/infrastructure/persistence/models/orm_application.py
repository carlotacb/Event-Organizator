from django.db import models


class ORMApplication(models.Model):
    class Meta:
        db_table = "application"

    id = models.UUIDField(primary_key=True)
    user = models.ForeignKey("ORMUser", on_delete=models.CASCADE)
    event = models.ForeignKey("ORMEvent", on_delete=models.CASCADE)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    options = models.CharField(max_length=255, null=True, default=None)
