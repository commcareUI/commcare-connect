# Generated by Django 4.2.5 on 2024-04-03 06:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("opportunity", "0038_opportunity_start_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="uservisit",
            name="is_trial",
            field=models.BooleanField(default=False),
        ),
    ]
