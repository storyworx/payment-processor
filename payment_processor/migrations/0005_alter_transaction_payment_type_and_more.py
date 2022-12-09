# Generated by Django 4.1.3 on 2022-11-29 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("payment_processor", "0004_alter_transaction_payment_type_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="transaction",
            name="payment_type",
            field=models.CharField(
                choices=[("CREDIT_CARD", "Credit card")], max_length=50
            ),
        ),
        migrations.AlterField(
            model_name="transaction",
            name="status",
            field=models.CharField(
                choices=[
                    ("INITIALIZED", "Initialized"),
                    ("REQUIRES_AUTHORIZATION", "Requires authorization"),
                    ("SUCCEDED", "Succeeded"),
                    ("FAILED", "Failed"),
                    ("CANCELLED", "Cancelled"),
                ],
                max_length=50,
            ),
        ),
        migrations.AlterField(
            model_name="transaction",
            name="transaction_type",
            field=models.CharField(
                choices=[
                    ("BUY", "Buy"),
                    ("SELL", "Sell"),
                    ("EXCHANGE", "Exchange"),
                    ("MINT", "Mint"),
                ],
                max_length=50,
            ),
        ),
    ]
