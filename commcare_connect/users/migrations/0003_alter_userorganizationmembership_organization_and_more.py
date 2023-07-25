# Generated by Django 4.2.1 on 2023-07-25 09:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0002_organization_userorganizationmembership"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userorganizationmembership",
            name="organization",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, related_name="memberships", to="users.organization"
            ),
        ),
        migrations.AlterField(
            model_name="userorganizationmembership",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING, related_name="memberships", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
