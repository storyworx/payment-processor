import enum


class ExtendedIntEnum(enum.IntEnum):
    @classmethod
    def list_values(cls):
        return list(map(lambda c: c.value, cls))

    @classmethod
    def list(cls):
        return list(map(lambda c: c, cls))

    def __contains__(cls, item):
        return item in cls.__members__


class StringEnum(str, enum.Enum):
    @classmethod
    def list_values(cls):
        return list(map(lambda c: c.value, cls))

    @classmethod
    def list(cls):
        return list(map(lambda c: c, cls))

    def __contains__(cls, item):
        return item in cls.__members__

    @classmethod
    def get_description(cls):
        return NotImplementedError

    @classmethod
    def choices(cls):
        return [(choice.value, choice.get_description()) for choice in cls]


class PaymentType(StringEnum):
    CREDIT_CARD = "CREDIT_CARD"

    def get_description(self):
        _descriptions = {
            self.CREDIT_CARD.value: "Credit card",
        }

        return _descriptions.get(self)


class TransactionType(StringEnum):
    BUY = "BUY"
    SELL = "SELL"
    EXCHANGE = "EXCHANGE"
    MINT = "MINT"

    def get_description(self):
        _descriptions = {
            self.BUY.value: "Buy",
            self.SELL.value: "Sell",
            self.EXCHANGE.value: "Exchange",
            self.MINT.value: "Mint",
        }

        return _descriptions.get(self)


class TransactionStatus(StringEnum):
    INITIALIZED = "INITIALIZED"
    REQUIRES_AUTHORIZATION = "REQUIRES_AUTHORIZATION"
    SUCCEEDED = "SUCCEDED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"

    def get_description(self):
        _descriptions = {
            self.INITIALIZED.value: "Initialized",
            self.REQUIRES_AUTHORIZATION.value: "Requires authorization",
            self.SUCCEEDED.value: "Succeeded",
            self.FAILED.value: "Failed",
            self.CANCELLED.value: "Cancelled",
        }

        return _descriptions.get(self)
