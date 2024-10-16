# Generated by Django 4.2.5 on 2024-10-07 08:54

from django.db import migrations, models, transaction

from commcare_connect.opportunity.utils.completed_work import update_work_payment_date


@transaction.atomic
def update_paid_date_from_payments(apps, schema_editor):
    OpportunityAccess = apps.get_model("opportunity.OpportunityAccess")
    Payment = apps.get_model("opportunity.Payment")
    CompletedWork = apps.get_model("opportunity.CompletedWork")
    accesses = OpportunityAccess.objects.all()
    for access in accesses:
        update_work_payment_date(access, Payment, CompletedWork)


class Migration(migrations.Migration):
    dependencies = [
        ("opportunity", "0059_payment_amount_usd"),
    ]

    operations = [
        migrations.AddField(
            model_name="completedwork",
            name="payment_date",
            field=models.DateTimeField(null=True),
        ),
        migrations.RunPython(update_paid_date_from_payments, migrations.RunPython.noop),
    ]
