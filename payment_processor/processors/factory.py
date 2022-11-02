from payment_processor.processors.stripe.processor import Stripe

from payment_processor import constants

PAYMENT_PROCESSORS_MAPPING = {
    constants.PaymentType.CREDIT_CARD: Stripe,
}


def get_processor(payment_type: constants.PaymentType):
    processor = PAYMENT_PROCESSORS_MAPPING.get(payment_type)
    if not processor:
        return None

    return processor()
