from payment_processor import constants


class BaseProcessor:
    def init_payment(
        self,
        user: int,
        base_amount: float,
        quote_amount: float,
        base_currency: str,
        quote_currency: str,
        payment_type: constants.PaymentType,
        transaction_type: constants.TransactionType,
    ) -> dict:
        raise NotImplementedError

    def process_payment(self):
        raise NotImplementedError
