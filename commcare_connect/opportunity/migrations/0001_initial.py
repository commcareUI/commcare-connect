# Generated by Django 4.2.1 on 2023-06-08 07:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("users", "0002_organization_userorganizationmembership"),
    ]

    operations = [
        migrations.CreateModel(
            name="Opportunity",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_by", models.CharField(max_length=255)),
                ("modified_by", models.CharField(max_length=255)),
                ("date_created", models.DateTimeField(auto_now_add=True)),
                ("date_modified", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=255)),
                ("description", models.TextField()),
                ("active", models.BooleanField(default=True)),
                (
                    "organization",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="opportunities",
                        related_query_name="opportunity",
                        to="users.organization",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
