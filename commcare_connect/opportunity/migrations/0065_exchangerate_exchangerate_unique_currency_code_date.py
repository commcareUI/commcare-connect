# Generated by Django 4.2.5 on 2025-01-07 10:26
import logging

from django.db import migrations, models
from django.db.models.functions import TruncDate

from commcare_connect.opportunity.visit_import import get_exchange_rate

logger = logging.getLogger(__name__)


def update_exchange_rate(apps, schema_editor):
    Payment = apps.get_model("opportunity.Payment")

    payments = (
        Payment.objects.annotate(date_only=TruncDate("date_paid"))
        .filter(payment_unit__opportunity__currency__isnull=False)
        .values(
            "id", "date_only", "amount", "opportunity_access__opportunity__currency", "invoice__opportunity__currency"
        )
        .distinct()
    )

    for payment in payments:
        date_paid = payment["date_only"]
        currency = payment["opportunity_access__opportunity__currency"] or payment["invoice__opportunity__currency"]

        if currency is "USD":
            exchange_rate = 1
        else:
            exchange_rate = get_exchange_rate(currency, date_paid)
            logger.info(
                f"Payment ID: {payment.id}, original USD: {payment.amount_usd}, USD acc. to new rate: {payment.amount / exchange_rate}"
            )
        if not exchange_rate:
            raise Exception(f"Invalid currency code {currency}")


class Migration(migrations.Migration):
    dependencies = [
        ("opportunity", "0064_alter_completedwork_unique_together"),
    ]

    operations = [
        migrations.CreateModel(
            name="ExchangeRate",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("currency_code", models.CharField(max_length=3)),
                ("rate", models.DecimalField(decimal_places=6, max_digits=10)),
                ("rate_date", models.DateField()),
                ("fetched_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddConstraint(
            model_name="exchangerate",
            constraint=models.UniqueConstraint(
                fields=("currency_code", "rate_date"), name="unique_currency_code_date"
            ),
        ),
        migrations.RunPython(update_exchange_rate, migrations.RunPython.noop),
    ]
