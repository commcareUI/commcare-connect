# Generated by Django 4.2.5 on 2024-10-03 02:33

from django.db import migrations, models
from django.db import transaction

from commcare_connect.opportunity.models import Payment
from commcare_connect.opportunity.visit_import import update_work_payment_date


@transaction.atomic
def update_paid_date_from_payments(apps, schema_editor):
    payments = Payment.objects.all()
    for payment in payments:
        update_work_payment_date(payment)


class Migration(migrations.Migration):
    dependencies = [
        ("opportunity", "0058_paymentinvoice_payment_invoice"),
    ]

    operations = [
        migrations.AddField(
            model_name="completedwork",
            name="payment_date",
            field=models.DateTimeField(null=True),
        ),
        migrations.RunPython(update_paid_date_from_payments, migrations.RunPython.noop),
    ]
