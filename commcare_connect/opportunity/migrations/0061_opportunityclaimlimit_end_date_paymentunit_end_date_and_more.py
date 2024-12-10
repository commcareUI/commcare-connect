# Generated by Django 4.2.5 on 2024-10-30 14:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("opportunity", "0060_completedwork_payment_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="opportunityclaimlimit",
            name="end_date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="paymentunit",
            name="end_date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="paymentunit",
            name="start_date",
            field=models.DateField(blank=True, null=True),
        ),
    ]
