# Generated by Django 4.0.1 on 2023-01-17 18:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('calculator_site', '0005_delete_businessusage_delete_conversionfactor'),
    ]

    operations = [
        migrations.RenameField(
            model_name='carbonfootprint',
            old_name='kitchen_equipment_asssets',
            new_name='kitchen_equipment_assets',
        ),
    ]
