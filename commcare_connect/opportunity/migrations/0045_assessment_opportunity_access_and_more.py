# Generated by Django 4.2.5 on 2024-05-27 08:08

from django.db import migrations, models
import django.db.models.deletion


def populate_opportunity_access(apps, schema_editor):
    OpportunityAccess = apps.get_model("opportunity.OpportunityAccess")
    CompletedModule = apps.get_model("opportunity.CompletedModule")
    Assessment = apps.get_model("opportunity.Assessment")
    UserVisit = apps.get_model("opportunity.UserVisit")

    access_objects = OpportunityAccess.objects.all()
    for access in access_objects:
        UserVisit.objects.filter(user=access.user, opportunity=access.opportunity).update(opportunity_access=access)
        CompletedModule.objects.filter(user=access.user, opportunity=access.opportunity).update(
            opportunity_access=access
        )
        Assessment.objects.filter(user=access.user, opportunity=access.opportunity).update(opportunity_access=access)


class Migration(migrations.Migration):
    dependencies = [
        ("opportunity", "0044_opportunityverificationflags"),
    ]

    operations = [
        migrations.AddField(
            model_name="assessment",
            name="opportunity_access",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.CASCADE, to="opportunity.opportunityaccess"
            ),
        ),
        migrations.AddField(
            model_name="completedmodule",
            name="opportunity_access",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.CASCADE, to="opportunity.opportunityaccess"
            ),
        ),
        migrations.AddField(
            model_name="uservisit",
            name="opportunity_access",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.CASCADE, to="opportunity.opportunityaccess"
            ),
        ),
        migrations.RunPython(populate_opportunity_access, migrations.RunPython.noop),
    ]
