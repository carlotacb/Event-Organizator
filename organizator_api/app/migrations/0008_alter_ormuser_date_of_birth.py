# Generated by Django 4.2.7 on 2024-01-06 21:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0007_alter_ormuser_date_of_birth_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ormuser",
            name="date_of_birth",
            field=models.DateTimeField(),
        ),
    ]