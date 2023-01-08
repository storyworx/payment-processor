import json
import logging

import requests
from circuitbreaker import circuit

from payment_processor.connectors import exceptions as connector_exceptions

logger = logging.getLogger(__name__)

LOGGER_PREFIX = "[SOLANA-CLIENT]"


class SolanaClient:
    base_url = "http://solana-client-service:3000/solana-client/api/v1"

    def get_wallets(self):
        url = f"{self.base_url}/wallets"
        response = requests.get(url)
        self._validate_response(response)
        data = response.json()

        logger.info(
            f"{LOGGER_PREFIX} GET response from {url}: \n {json.dumps(data, indent=2)}"
        )

        return data

    @circuit(failure_threshold=5, recovery_timeout=30)
    def create_account(self, user_id: int):
        payload = {"userId": user_id}
        url = f"{self.base_url}/create-account"
        response = requests.post(url, json=payload)
        self._validate_response(response)
        data = response.json()

        logger.info(
            f"{LOGGER_PREFIX} POST response from {url}: \n {json.dumps(data, indent=2)}"
        )

        return data

    @circuit(failure_threshold=5, recovery_timeout=30)
    def create_token(self, user_id: int):
        payload = {"userId": user_id}
        url = f"{self.base_url}/create-token"
        response = requests.post(url, json=payload)
        self._validate_response(response)
        data = response.json()

        logger.info(
            f"{LOGGER_PREFIX} POST response from {url}: \n {json.dumps(data, indent=2)}"
        )

        return data

    @circuit(failure_threshold=5, recovery_timeout=30)
    def mint_token(self, owner_id: int, destination_id: int, token: str, amount: int):
        payload = {
            "ownerId": owner_id,
            "destinationId": destination_id,
            "token": token,
            "amount": amount,
        }
        url = f"{self.base_url}/mint-token"
        response = requests.post(url, json=payload)
        self._validate_response(response)
        data = response.json()

        logger.info(
            f"{LOGGER_PREFIX} POST response from {url}: \n {json.dumps(data, indent=2)}"
        )

        return data

    def _validate_response(self, response: requests.Response):
        if response.status_code != 200:
            raise connector_exceptions.SolanaClientException(
                f"Response code {response.status_code}"
            )
