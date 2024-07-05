# Generated by Django 4.2.5 on 2024-07-05 04:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("opportunity", "0049_deliverytype_opportunity_delivery_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="opportunityverificationflags",
            name="catchment_areas",
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name="CatchmentArea",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("latitude", models.DecimalField(decimal_places=8, max_digits=10)),
                ("longitude", models.DecimalField(decimal_places=8, max_digits=11)),
                ("radius", models.IntegerField(default=1000)),
                ("active", models.BooleanField(default=True)),
                ("name", models.CharField(max_length=255)),
                (
                    "opportunity",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="opportunity.opportunity"),
                ),
                (
                    "opportunity_access",
                    models.ForeignKey(
                        null=True, on_delete=django.db.models.deletion.DO_NOTHING, to="opportunity.opportunityaccess"
                    ),
                ),
            ],
        ),
    ]
