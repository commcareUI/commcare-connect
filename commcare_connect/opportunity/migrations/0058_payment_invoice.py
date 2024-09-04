# Generated by Django 4.2.5 on 2024-09-05 04:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("opportunity", "0057_paymentinvoice"),
    ]

    operations = [
        migrations.AddField(
            model_name="payment",
            name="invoice",
            field=models.OneToOneField(
                blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to="opportunity.paymentinvoice"
            ),
        ),
    ]
