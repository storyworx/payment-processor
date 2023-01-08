import logging

from payment_processor import constants

logger = logging.getLogger(__name__)


class BaseProcessor:
    LOGGER_PREFIX = "[BASE-PROCESSOR]"

    def init_payment(
        self,
        user_id: int,
        base_amount: float,
        quote_amount: float,
        base_currency: str,
        quote_currency: str,
        payment_type: constants.PaymentType,
        transaction_type: constants.TransactionType,
    ) -> dict:
        raise NotImplementedError

    def process_payment(self, user_id: int, txid: str, status: str):
        raise NotImplementedError

    def make_token_transaction(self, buyer: id, seller: id, amount: int, token: str):
        from payment_processor.tasks import make_token_transaction

        make_token_transaction.apply_async((buyer, seller, amount, token))

    def log(self, message, log_type="info"):
        if log_type == "warning":
            logger.warning(f"{self.LOGGER_PREFIX} {message}")
        elif log_type == "error":
            logger.error(f"{self.LOGGER_PREFIX} {message}")
        else:
            logger.info(f"{self.LOGGER_PREFIX} {message}")
