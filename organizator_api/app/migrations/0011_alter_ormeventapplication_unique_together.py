# Generated by Django 4.2.7 on 2024-01-08 11:35

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0010_ormeventapplication_deleted_at"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="ormeventapplication",
            unique_together={("user", "event")},
        ),
    ]