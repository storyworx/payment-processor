from payment_processor import constants

INTENT_STATUS_REQUIRES_ACTION = "requires_action"
INTENT_STATUS_USE_STRIPE_SDK = "use_stripe_sdk"
INTENT_STATUS_SUCCESS = "succeeded"

PAYMENT_METHODS_MAP = {"card": constants.PaymentType.CREDIT_CARD}
