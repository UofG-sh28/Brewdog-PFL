# Generated by Django 4.1 on 2023-03-17 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("calculator_site", "0021_alter_actionplandetail_end_date_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="actionplandetail",
            name="end_date",
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name="actionplandetail",
            name="start_date",
            field=models.DateTimeField(null=True),
        ),
    ]