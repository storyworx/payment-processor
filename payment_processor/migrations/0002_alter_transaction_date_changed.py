# Generated by Django 4.1.3 on 2022-12-30 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("payment_processor", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="transaction",
            name="date_changed",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
