# Generated by Django 4.2.8 on 2024-12-29 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('algaecide', '0054_remove_predictiontask_smiles_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='algaespecies',
            name='image_copyright',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='chemical',
            name='image_copyright',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
