import json
import logging

from django.conf import settings
from django.core.management.base import BaseCommand
from kafka import KafkaConsumer

from payment_processor.tasks import tasks as payment_processor_tasks

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Closes the specified poll for voting"
    LOGGER_PREFIX = ["STRIPE-WORKER-COMMAND"]

    def add_arguments(self, parser):
        parser.add_argument("-p", "--partition", nargs="?", type=int, default=0)

    def handle(self, *args, **options):
        # partition = options["partition"]
        topic = "complete-stripe-payment"

        consumer = KafkaConsumer(topic, bootstrap_servers=f"{settings.KAFKA_HOST}:9092")

        while True:
            try:
                msg = next(consumer)
                payment_details = json.loads(msg.value)
                payment_processor_tasks.complete_stripe_payment.apply_async(
                    (
                        payment_details["txid"],
                        payment_details["id"],
                        payment_details["amount"],
                        payment_details["status"],
                    )
                )

            except Exception as e:
                logger.error(f"{self.LOGGER_PREFIX} {e}")
