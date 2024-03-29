# Generated by Django 4.2.7 on 2024-01-10 00:09

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0013_ormevent_age_restrictions_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ormevent",
            name="age_restrictions",
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name="ormevent",
            name="expected_attrition_rate",
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name="ormevent",
            name="max_participants",
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name="ormevent",
            name="open_for_participants",
            field=models.BooleanField(default=True),
        ),
    ]
