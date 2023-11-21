from django.db import models


class ORMEvent(models.Model):
    class Meta:
        db_table = "event"

    id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    url = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    location = models.CharField(max_length=255)
    header_image = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    deleted_at = models.DateTimeField(null=True)
