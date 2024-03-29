# Generated by Django 4.2.7 on 2023-11-21 16:09

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ORMEvent",
            fields=[
                ("id", models.UUIDField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=255, unique=True)),
                ("url", models.CharField(max_length=255)),
                ("description", models.TextField()),
                ("start_date", models.DateTimeField()),
                ("end_date", models.DateTimeField()),
                ("location", models.CharField(max_length=255)),
                ("header_image", models.CharField(max_length=255)),
                ("created_at", models.DateTimeField()),
                ("updated_at", models.DateTimeField()),
                ("deleted_at", models.DateTimeField(null=True)),
            ],
            options={
                "db_table": "event",
            },
        ),
    ]
