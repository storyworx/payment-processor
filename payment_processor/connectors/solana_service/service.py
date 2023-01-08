import logging
import typing

from payment_processor.connectors import exceptions as connector_exceptions
from payment_processor.connectors.solana_service import client as solana_client

LOGGER_PREFIX = "[SOLANA-SERVICE]"

logger = logging.getLogger(__name__)


class Solana:
    def __init__(self, *args, **kwargs):
        self.client = solana_client.SolanaClient()

    def complete_buy(
        self,
        owner_id: int,
        destination_id: int,
        amount: int,
        token: typing.Optional[str] = None,
    ):
        try:
            existing_wallets = self.client.get_wallets()
        except connector_exceptions.SolanaClientException as e:
            raise connector_exceptions.SolanaProcessorException(str(e))

        if destination_id not in existing_wallets:
            try:
                self.client.create_account(destination_id)
            except connector_exceptions.SolanaClientException as e:
                raise connector_exceptions.SolanaProcessorException(str(e))

        if token:
            if owner_id not in existing_wallets:
                raise connector_exceptions.SolanaProcessorException(
                    f"{LOGGER_PREFIX} owner_id={owner_id} doesn't have a wallet"
                )

            try:
                self.client.mint_token(owner_id, destination_id, token, amount)
            except connector_exceptions.SolanaClientException as e:
                raise connector_exceptions.SolanaProcessorException(str(e))

        else:
            if owner_id != destination_id:
                raise connector_exceptions.SolanaProcessorException(
                    (
                        f"{LOGGER_PREFIX} owner and destination"
                        f"should be same when minting new token"
                    )
                )

            try:
                token = self.client.create_token(owner_id).get("token")
                self.client.mint_token(owner_id, destination_id, token, amount)
            except connector_exceptions.SolanaClientException as e:
                raise connector_exceptions.SolanaProcessorException(str(e))
