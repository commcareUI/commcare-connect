# Generated by Django 4.2.5 on 2024-04-18 09:43

from django.db import migrations, models


def migrate_trial(apps, schema_editor):
    UserVisit = apps.get_model("opportunity.UserVisit")
    UserVisit.objects.filter(is_trial=True).update(status='trial')


def migrate_trial_rev(apps, schema_editor):
    UserVisit = apps.get_model("opportunity.UserVisit")
    UserVisit.objects.filter(status='trial').update(is_trial=True)


class Migration(migrations.Migration):
    dependencies = [
        ("opportunity", "0042_bulk_approve_completed_work"),
    ]

    operations = [
        migrations.AlterField(
            model_name="uservisit",
            name="status",
            field=models.CharField(
                choices=[
                    ("pending", "Pending"),
                    ("approved", "Approved"),
                    ("rejected", "Rejected"),
                    ("over_limit", "Over Limit"),
                    ("duplicate", "Duplicate"),
                    ("trial", "Trial"),
                ],
                default="pending",
                max_length=50,
            ),
        ),
        migrations.RunPython(
            migrate_trial,
            migrate_trial_rev,
            hints={"run_on_secondary": False}
        ),
        migrations.RemoveField(
            model_name="uservisit",
            name="is_trial",
        ),
    ]
