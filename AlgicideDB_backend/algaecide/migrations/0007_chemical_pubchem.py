# Generated by Django 4.2.8 on 2024-09-24 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("algaecide", "0006_remove_reference_publishing_time_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="chemical",
            name="pubchem",
            field=models.URLField(blank=True, null=True),
        ),
    ]
