# Generated by Django 4.2.5 on 2024-03-12 10:53

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("opportunity", "0033_completedwork_uservisit_completed_work"),
    ]

    operations = [
        migrations.AddField(
            model_name="deliverunit",
            name="optional",
            field=models.BooleanField(default=False),
        ),
    ]
