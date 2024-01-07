# Generated by Django 4.2.7 on 2024-01-07 19:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0008_alter_ormuser_date_of_birth"),
    ]

    operations = [
        migrations.CreateModel(
            name="ORMApplication",
            fields=[
                ("id", models.UUIDField(primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField()),
                ("updated_at", models.DateTimeField()),
                ("options", models.CharField(default=None, max_length=255, null=True)),
                (
                    "event_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="app.ormevent"
                    ),
                ),
                (
                    "user_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="app.ormuser"
                    ),
                ),
            ],
            options={
                "db_table": "application",
            },
        ),
    ]
