# Generated by Django 4.2.8 on 2024-11-21 03:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('algaecide', '0038_algaespecies_empire_algaespecies_kingdom'),
    ]

    operations = [
        migrations.AddField(
            model_name='algaespecies',
            name='algaebaselink',
            field=models.URLField(blank=True, null=True),
        ),
    ]
