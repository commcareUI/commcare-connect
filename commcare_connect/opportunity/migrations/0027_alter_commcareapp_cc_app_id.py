# Generated by Django 4.2.5 on 2023-11-22 21:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("opportunity", "0026_create_send_inactive_notification_periodic_task"),
    ]

    operations = [
        migrations.AlterField(
            model_name="commcareapp",
            name="cc_app_id",
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
