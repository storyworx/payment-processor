from core import settings
from payment_processor import constants
from payment_processor.models import Transaction
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
        user,
        base_amount,
        quote_amount,
        base_currency,
        quote_currency,
        payment_type: constants.PaymentType,
        transaction_type: constants.TransactionType,
    ):

        external_id, client_secret = self.client.create_payment_intent(
            base_amount, base_currency
        )

        Transaction.objects.create(
            buyer=user,
            payment_type=payment_type,
            transaction_type=transaction_type,
            status=constants.TransactionStatus.INITIALIZED,
            base_currency=base_currency,
            quote_currency=quote_currency,
            base_amount=base_amount,
            quote_amount=quote_amount,
            external_id=external_id,
        )

        return {"client_secret": client_secret}

    def process_payment(self, user, txid):

        pass
