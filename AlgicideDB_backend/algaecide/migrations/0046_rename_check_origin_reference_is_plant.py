# Generated by Django 4.2.8 on 2024-12-16 01:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("algaecide", "0045_reference_check_origin"),
    ]

    operations = [
        migrations.RenameField(
            model_name="reference",
            old_name="check_origin",
            new_name="is_plant",
        ),
    ]
