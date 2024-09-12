# Generated by Django 4.2.5 on 2024-10-03 17:40

from django.db import migrations, models
from django.db.models.functions import TruncDate
from commcare_connect.opportunity.visit_import import get_exchange_rate

def populate_amount_usd():
    Payment = apps.get_model("opportunity.Payment")
    payments = (
        Payment.objects
        .annotate(date_only=TruncDate('date_paid'))
        .values('date_only', 'opportunity_access__opportunity__currency')
        .distinct()
    )

    for payment in payments:
        date_paid = payment['date_only']
        currency = payment['opportunity_access__opportunity__currency']

        if currency in ['USD', None]:
            exchange_rate = 1
        else:
            exchange_rate = get_exchange_rate(currency, date_paid)
        if not exchange_rate:
            raise Exception(f"Invalid currency code {currency}")

        payments_to_update = Payment.objects.filter(
            date_paid=date_paid,
            opportunity_access__opportunity__currency=currency
        )
        payments_to_update.update(amount_usd=models.F('amount') / exchange_rate)


class Migration(migrations.Migration):
    dependencies = [
        ("opportunity", "0054_formjsonvalidationrules_deliverunitflagrules"),
    ]

    operations = [
        migrations.AddField(
            model_name="payment",
            name="amount_usd",
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.RunPython(populate_amount_usd, migrations.RunPython.noop)
    ]
