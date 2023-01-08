from django.db import transaction

from conf import settings
from payment_processor import constants
from payment_processor import models as payment_processor_models
from payment_processor.processors import exceptions as payment_processor_exceptions
from payment_processor.processors.base.processor import BaseProcessor
from payment_processor.processors.stripe import client as stripe_client
from payment_processor.processors.stripe import metrics as stripe_metrics


class Stripe(BaseProcessor):
    LOGGER_PREFIX = "[STRIPE-PROCESSOR]"

    def __init__(self) -> None:
        self.stripe_credentials = settings.StripeCredentials()
        self.client = self._init_client()

    def _init_client(self):
        return stripe_client.StripeClient(
            self.stripe_credentials.STRIPE_API_KEY,
            self.stripe_credentials.STRIPE_API_SECRET,
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

            self.log(f"Payment intent (id={intent_id}) created.")

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

            self.log(f"Transaction (id={tx.txid}) {tx.status.get_description()}.")

            self.client.add_payment_intent_metadata(intent_id, {"txid": tx.txid})

            self.log(
                f"Payment intent (id={intent_id}) updated with transaction metadata"
            )

        return {"client_secret": client_secret}

    def process_payment(self, txid, status):

        with transaction.atomic():
            tx = (
                payment_processor_models.Transaction.objects.filter(
                    txid=txid, status=constants.TransactionStatus.INITIALIZED
                )
                .select_for_update()
                .first()
            )
            if tx is None:
                msg = f"transaction (txid={txid}) with status INITIALIZED not found"
                self.log(msg, log_type="error")
                raise payment_processor_exceptions.StripeProcessorException(msg)

            try:
                init_time = tx.date_changed
                tx.status = constants.TransactionStatus[status]
                tx.save()
                elapsed = (tx.date_changed - init_time).seconds
                stripe_metrics.send_stripe_elapsed_time(elapsed)
                self.log(
                    (
                        f"transaction (txid={txid}) processed with status: "
                        f"{tx.status}, elapsed time: {elapsed}s"
                    )
                )
                if tx.status == constants.TransactionStatus.SUCCEEDED:
                    self.log(
                        (
                            f"making token buy transaction (txid={txid}), (buyer={tx.buyer}), "
                            f"(amount={tx.quote_amount}), (token={tx.quote_currency})"
                        )
                    )
                    self.make_token_transaction(
                        tx.buyer, tx.buyer, tx.quote_amount, tx.quote_currency
                    )

            except KeyError:
                self.log(
                    f"status {status} is not a valid TransactionStatus",
                    log_type="error",
                )
