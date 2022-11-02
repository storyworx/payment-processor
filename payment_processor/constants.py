import enum


class ExtendedEnum(enum.Enum):
    @classmethod
    def list_values(cls):
        return list(map(lambda c: c.value, cls))

    @classmethod
    def list(cls):
        return list(map(lambda c: c, cls))

    def __contains__(cls, item):
        return item in cls.__members__


class PaymentType(ExtendedEnum):
    CREDIT_CARD = "CREDIT_CARD"


PAYMENT_TYPES = ((PaymentType.CREDIT_CARD, "Credit Card"),)


class TransactionType(ExtendedEnum):
    BUY = "BUY"
    SELL = "SELL"
    EXCHANGE = "EXCHANGE"


TRANSACTION_TYPES = (
    (TransactionType.BUY, "Buy"),
    (TransactionType.SELL, "Sell"),
    (TransactionType.EXCHANGE, "Exchange"),
)


class TransactionStatus(ExtendedEnum):
    INITIALIZED = 1
    REQUIRES_AUTHORIZATION = 2
    SUCCEEDED = 3
    FAILED = 4
    CANCELLED = 5


TRANSACTION_STATUSES = (
    (TransactionStatus.INITIALIZED, "Initialized"),
    (TransactionStatus.SUCCEEDED, "Succeeded"),
    (TransactionStatus.REQUIRES_AUTHORIZATION, "Requires authorization"),
)
