# Generated by Django 4.2.7 on 2024-01-11 18:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0014_alter_ormevent_age_restrictions_and_more"),
    ]

    operations = [
        migrations.AddField(
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
                ],
                default="PENDING",
                max_length=255,
            ),
        ),
    ]