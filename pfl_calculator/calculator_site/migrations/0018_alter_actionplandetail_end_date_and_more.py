# Generated by Django 4.1 on 2023-03-17 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("calculator_site", "0017_alter_actionplandetail_end_date_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="actionplandetail",
            name="end_date",
            field=models.DateField(default="2000-01-01"),
        ),
        migrations.AlterField(
            model_name="actionplandetail",
            name="plan_detail",
            field=models.TextField(default="", max_length=200),
        ),
        migrations.AlterField(
            model_name="actionplandetail",
            name="start_date",
            field=models.DateField(default="2000-01-01"),
        ),
    ]
