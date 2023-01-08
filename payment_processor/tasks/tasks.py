import logging
import typing

from celery import shared_task

from payment_processor import constants
from payment_processor.processors import exceptions as payment_processor_exceptions

logger = logging.getLogger(__name__)


@shared_task(bind=True)
def complete_stripe_payment(
    self, txid: str, payment_intent: str, amount: int, status: str
):
    from payment_processor.processors.factory import get_processor

    try:
        processor = get_processor(constants.PaymentType.CREDIT_CARD.value)
        processor.process_payment(txid=txid, status=status)
    except payment_processor_exceptions.StripeProcessorException:
        return


@shared_task(bind=True)
def make_token_transaction(
    self,
    owner_id: int,
    destination_id: int,
    amount: int,
    token: typing.Optional[str] = None,
):
    from payment_processor.connectors import exceptions as connector_exceptions
    from payment_processor.connectors.solana_service import service as solana_service

    service = solana_service.Solana()
    try:
        service.complete_buy(
            owner_id=owner_id, destination_id=destination_id, amount=amount, token=token
        )
    except connector_exceptions.SolanaProcessorException as e:
        logger.error(str(e))
        raise self.retry(exc=e, max_retries=10)
