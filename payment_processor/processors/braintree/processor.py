from django.db import transaction

from conf import settings
from payment_processor import constants
from payment_processor import models as payment_processor_models
from payment_processor.processors import exceptions as payment_processor_exceptions
from payment_processor.processors.base.processor import BaseProcessor
from payment_processor.processors.braintree import client as braintree_client
from payment_processor.processors.braintree import constants as braintree_constants
from payment_processor.processors.braintree import parsers as braintree_parsers


class Braintree(BaseProcessor):
    LOGGER_PREFIX = "[BRAINTREE-PROCESSOR]"

    def __init__(self, currency: str = "USD") -> None:
        self.braintree_credentials = settings.BraintreeCredentials()
        self.client = self._init_client(currency)

    def _init_client(self, currency: str):
        return braintree_client.BraintreeClient(
            self.braintree_credentials.URL,
            self.braintree_credentials.MERCHANT_ID,
            self.braintree_credentials.MERCHANT_ACCOUNT_IDS[currency],
            self.braintree_credentials.API_KEY,
            self.braintree_credentials.API_SECRET,
            self.braintree_credentials.API_VERSION,
        )

    def create_client_token(self):
        data = self.client.create_client_token()
        client_token = braintree_parsers.parse_client_token(data)
        return {"client_token": client_token}

    def init_payment(
        self,
        user_id: int,
        base_amount: float,
        quote_amount: float,
        base_currency: str,
        quote_currency: str,
        payment_type: constants.PaymentType,
        transaction_type: constants.TransactionType,
        payment_method_id: str,
    ) -> dict:
        with transaction.atomic():
            data = self.client.charge_payment_method(payment_method_id, base_amount)
            transaction_id = braintree_parsers.parse_transaction_id(data)
            transaction_status = braintree_parsers.parse_transaction_status(data)

            self.log(
                f"Charge (id={transaction_id}) created. Status {transaction_status}"
            )

            tx = payment_processor_models.Transaction.objects.create(
                buyer=user_id,
                payment_type=payment_type,
                transaction_type=transaction_type,
                status=constants.TransactionStatus.INITIALIZED,
                base_currency=base_currency,
                quote_currency=quote_currency,
                base_amount=base_amount,
                quote_amount=quote_amount,
                external_id=transaction_id,
            )

            self.log(f"Transaction (id={tx.txid}) {tx.status.get_description()}.")

        if transaction_status in braintree_constants.TRANSACTION_SUCCESS_STATUSES:
            status = constants.TransactionStatus.SUCCEEDED.value
        else:
            status = constants.TransactionStatus.FAILED.value

        return {"txid": tx.txid, "status": status}

    def process_payment(self, txid: str, status: str):
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
                raise payment_processor_exceptions.BraintreeClientException(msg)

            tx.status = constants.TransactionStatus[status]
            tx.save()
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
