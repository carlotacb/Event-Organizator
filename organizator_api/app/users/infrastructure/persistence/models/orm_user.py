from django.db import models

from app.users.domain.models.user import UserRoles, TShirtSizes, GenderOptions


class ORMUser(models.Model):
    class Meta:
        db_table = "user"

    id = models.UUIDField(primary_key=True)
    email = models.CharField(max_length=255, unique=True)
    password = models.BinaryField()
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True)
    bio = models.TextField()
    profile_image = models.CharField(max_length=255)
    token = models.UUIDField(default=None, null=True)
    role = models.CharField(
        max_length=120, choices=UserRoles.choices(), default="Participant"
    )
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    tshirt = models.CharField(max_length=120, choices=TShirtSizes.choices(), null=True, default=None)
    alimentary_restrictions = models.CharField(max_length=255, null=True, default=None)
    date_of_birth = models.DateField(null=True, default=None)
    study = models.BooleanField(default=False)
    work = models.BooleanField(default=False)
    gender = models.CharField(max_length=120, choices=GenderOptions.choices(), null=True, default=None)
    github = models.CharField(max_length=255, null=True, default=None)
    linkedin = models.CharField(max_length=255, null=True, default=None)
    devpost = models.CharField(max_length=255, null=True, default=None)
    webpage = models.CharField(max_length=255, null=True, default=None)
    university = models.CharField(max_length=255, null=True, default=None)
    degree = models.CharField(max_length=255, null=True, default=None)
    expected_graduation = models.DateField(null=True, default=None)
    current_job_role = models.CharField(max_length=255, null=True, default=None)
