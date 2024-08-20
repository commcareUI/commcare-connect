# Generated by Django 4.2.5 on 2024-08-20 05:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("opportunity", "0054_opportunity_managed_alter_opportunity_organization"),
        ("organization", "0006_organization_program_manager"),
    ]

    operations = [
        migrations.CreateModel(
            name="ManagedOpportunity",
            fields=[
                (
                    "opportunity_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="opportunity.opportunity",
                    ),
                ),
                ("claimed", models.BooleanField(default=False)),
                ("org_pay_per_visit", models.IntegerField(null=True)),
            ],
            options={
                "abstract": False,
            },
            bases=("opportunity.opportunity",),
        ),
        migrations.CreateModel(
            name="Program",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_by", models.CharField(max_length=255)),
                ("modified_by", models.CharField(max_length=255)),
                ("date_created", models.DateTimeField(auto_now_add=True)),
                ("date_modified", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=255)),
                ("slug", models.SlugField(max_length=255, unique=True)),
                ("description", models.CharField()),
                ("budget", models.IntegerField()),
                ("currency", models.CharField(max_length=3)),
                ("start_date", models.DateField()),
                ("end_date", models.DateField()),
                (
                    "delivery_type",
                    models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="opportunity.deliverytype"),
                ),
                (
                    "organization",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="organization.organization"),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="ManagedOpportunityApplication",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_by", models.CharField(max_length=255)),
                ("modified_by", models.CharField(max_length=255)),
                ("date_created", models.DateTimeField(auto_now_add=True)),
                ("date_modified", models.DateTimeField(auto_now=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("invited", "Invited"),
                            ("applied", "Applied"),
                            ("accepted", "Accepted"),
                            ("rejected", "Rejected"),
                        ],
                        default="invited",
                        max_length=20,
                    ),
                ),
                (
                    "managed_opportunity",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="program.managedopportunity"),
                ),
                (
                    "organization",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="organization.organization"),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="managedopportunity",
            name="program",
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to="program.program"),
        ),
    ]
