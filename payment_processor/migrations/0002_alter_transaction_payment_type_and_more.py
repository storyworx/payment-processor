# Generated by Django 4.1.3 on 2022-11-16 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("payment_processor", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="transaction",
            name="payment_type",
            field=models.IntegerField(choices=[("0", "Credit Card")]),
        ),
        migrations.AlterField(
            model_name="transaction",
            name="status",
            field=models.IntegerField(
                choices=[
                    ("1", "Initialized"),
                    ("2", "Requires Authorization"),
                    ("3", "Succeeded"),
                    ("4", "Failed"),
                    ("5", "Cancelled"),
                ]
            ),
        ),
        migrations.AlterField(
            model_name="transaction",
            name="transaction_type",
            field=models.IntegerField(
                choices=[("0", "Buy"), ("1", "Sell"), ("2", "Exchange")]
            ),
        ),
    ]
