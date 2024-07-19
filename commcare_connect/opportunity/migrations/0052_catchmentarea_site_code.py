# Generated by Django 4.2.5 on 2024-07-19 08:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("opportunity", "0051_opportunityverificationflags_catchment_areas_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="catchmentarea",
            name="site_code",
            field=models.SlugField(blank=True, max_length=255, unique=True),
        ),
    ]
