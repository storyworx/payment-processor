import typing

import stripe

from payment_processor.processors import exceptions as payment_processor_exceptions
from payment_processor.processors.stripe import constants as stripe_constants


class StripeClient:
    def __init__(self, api_key: str, secret_key: str) -> None:
        self.api_key = api_key
        stripe.api_key = secret_key
        # stripe.betas = "server_side_confirmation_beta_1"
        stripe.api_version = "2022-08-01"

    def create_payment_intent(
        self,
        amount: float,
        currency: str,
    ) -> typing.Tuple[bool, str]:

        intent = stripe.PaymentIntent.create(
            amount=int(amount * 100),
            currency=currency,
            payment_method_types=["card"],
        )

        return (intent.id, intent.client_secret)

    def add_payment_intent_metadata(self, id: str, metadata: dict):
        stripe.PaymentIntent.modify(id, metadata=metadata)

    def confirm_payment_intent(self, payment_intent_id: str) -> typing.Tuple[bool, str]:
        intent = stripe.PaymentIntent.confirm(
            payment_intent_id, api_key=self.secret_key
        )

        result = self._handle_intent_status(intent)
        return result

    def _handle_intent_status(self, intent) -> typing.Tuple[bool, str]:
        if (
            intent.status == stripe_constants.INTENT_STATUS_REQUIRES_ACTION
            and intent.next_action.type == stripe_constants.INTENT_STATUS_USE_STRIPE_SDK
        ):
            requires_action = True
            payment_intent_client_secret = intent.client_secret

        elif intent.status == stripe_constants.INTENT_STATUS_SUCCESS:
            requires_action = False
            payment_intent_client_secret = ""

        else:
            msg = "Failed creating payment intent with status: {}".format(intent.status)
            raise payment_processor_exceptions.StripeClientException(msg)

        return (requires_action, payment_intent_client_secret)
