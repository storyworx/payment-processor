import uuid

from django.db import models
from django.db.models import CheckConstraint, Q

from payment_processor import constants


class Transaction(models.Model):
    txid = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, primary_key=True
    )  # models.CharField(max_length=50, blank=False, null=False, primary_key=True)

    external_id = models.CharField(max_length=50, blank=True, null=True, unique=True)

    buyer = models.IntegerField(
        blank=False,
        null=False,
    )
    seller = models.IntegerField(
        blank=True,
        null=True,
    )
    payment_type = models.CharField(
        max_length=50,
        blank=False,
        null=False,
        choices=constants.PaymentType.choices(),
    )
    transaction_type = models.CharField(
        max_length=50,
        blank=False,
        null=False,
        choices=constants.TransactionType.choices(),
    )
    status = models.CharField(
        max_length=50,
        blank=False,
        null=False,
        choices=constants.TransactionStatus.choices(),
    )
    base_currency = models.CharField(max_length=100, blank=False, null=False)
    quote_currency = models.CharField(max_length=100, blank=False, null=False)

    base_amount = models.FloatField(blank=False, null=False)
    quote_amount = models.FloatField(blank=False, null=False)

    class Meta:
        constraints = (
            # for checking in the DB
            CheckConstraint(
                check=Q(base_amount__gte=0.0) & Q(quote_amount__gte=0.0),
                name="positive_amounts",
            ),
        )
