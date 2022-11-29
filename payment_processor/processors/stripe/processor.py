from django.conf import settings
from django.db import transaction

from payment_processor import constants
from payment_processor import models as payment_processor_models
from payment_processor.processors.base.processor import BaseProcessor
from payment_processor.processors.stripe import client as stripe_client


class Stripe(BaseProcessor):
    def __init__(self) -> None:
        self.client = self._init_client()

    def _init_client(self):
        return stripe_client.StripeClient(
            settings.STRIPE_API_KEY, settings.STRIPE_API_SECRET
        )

    def init_payment(
        self,
        user_id,
        base_amount,
        quote_amount,
        base_currency,
        quote_currency,
        payment_type: str,
        transaction_type: constants.TransactionType,
    ):

        with transaction.atomic():

            intent_id, client_secret = self.client.create_payment_intent(
                base_amount, base_currency
            )

            payment_type = constants.PaymentType[payment_type]

            tx = payment_processor_models.Transaction.objects.create(
                buyer=user_id,
                payment_type=payment_type,
                transaction_type=transaction_type,
                status=constants.TransactionStatus.INITIALIZED,
                base_currency=base_currency,
                quote_currency=quote_currency,
                base_amount=base_amount,
                quote_amount=quote_amount,
                external_id=intent_id,
            )

            self.client.add_payment_intent_metadata(intent_id, {"txit": tx.txid})

        return {"client_secret": client_secret}

    def process_payment(self, txid):
        transaction = payment_processor_models.Transaction.objects.filter(
            txid=txid
        ).first()
        transaction.update(status=constants.TransactionStatus.SUCCEEDED)
