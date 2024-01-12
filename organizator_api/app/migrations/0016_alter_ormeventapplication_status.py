# Generated by Django 4.2.7 on 2024-01-12 23:42

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0015_ormeventapplication_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ormeventapplication",
            name="status",
            field=models.CharField(
                choices=[
                    ("PENDING", "Under review"),
                    ("INVITED", "Invited"),
                    ("CONFIRMED", "Confirmed"),
                    ("CANCELLED", "Cancelled"),
                    ("INVALID", "Invalid"),
                    ("REJECTED", "Rejected"),
                    ("WAIT_LIST", "Wait list"),
                    ("ATTENDED", "Attended"),
                ],
                default="PENDING",
                max_length=255,
            ),
        ),
    ]
