# Generated by Django 4.1.3 on 2022-11-16 20:21

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Transaction",
            fields=[
                (
                    "txid",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                (
                    "external_id",
                    models.CharField(blank=True, max_length=50, null=True, unique=True),
                ),
                ("buyer", models.IntegerField()),
                ("seller", models.IntegerField(blank=True, null=True)),
                (
                    "payment_type",
                    models.CharField(choices=[("0", "CREDIT_CARD")], max_length=50),
                ),
                (
                    "transaction_type",
                    models.CharField(
                        choices=[("0", "BUY"), ("1", "SELL"), ("2", "EXCHANGE")],
                        max_length=50,
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("1", "INITIALIZED"),
                            ("2", "REQUIRES_AUTHORIZATION"),
                            ("3", "SUCCEEDED"),
                            ("4", "FAILED"),
                            ("5", "CANCELLED"),
                        ],
                        max_length=50,
                    ),
                ),
                ("base_currency", models.CharField(max_length=100)),
                ("quote_currency", models.CharField(max_length=100)),
                ("base_amount", models.FloatField()),
                ("quote_amount", models.FloatField()),
            ],
        ),
        migrations.AddConstraint(
            model_name="transaction",
            constraint=models.CheckConstraint(
                check=models.Q(("base_amount__gte", 0.0), ("quote_amount__gte", 0.0)),
                name="positive_amounts",
            ),
        ),
    ]
