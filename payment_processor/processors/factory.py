from payment_processor import constants
from payment_processor.processors.stripe.processor import Stripe

PAYMENT_PROCESSORS_MAPPING = {
    constants.PaymentType.CREDIT_CARD: Stripe,
}


def get_processor(payment_type: str):
    try:
        payment_type = constants.PaymentType[payment_type]
    except KeyError:
        return None

    processor = PAYMENT_PROCESSORS_MAPPING.get(payment_type)
    if not processor:
        return None

    return processor()
