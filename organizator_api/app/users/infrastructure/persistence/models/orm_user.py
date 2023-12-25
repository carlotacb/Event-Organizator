from django.db import models


class ORMUser(models.Model):
    class Meta:
        db_table = "user"

    id = models.UUIDField(primary_key=True)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True)
    bio = models.TextField()
    profile_image = models.CharField(max_length=255)
    token = models.UUIDField(default=None, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
