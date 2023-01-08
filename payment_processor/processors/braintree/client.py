import base64

import requests

from payment_processor.processors import exceptions as payment_processor_exceptions

LOGGER_PREFIX = "[BRAINTREE-CLIENT]"


class BraintreeClient:
    def __init__(
        self,
        url: str,
        merchant_id: str,
        merchant_account_id: str,
        api_key: str,
        api_secret: str,
        api_version: str,
    ) -> None:
        self.url = url
        self.merchant_id = merchant_id
        self.merchant_account_id = merchant_account_id
        self.api_key = api_key
        self.api_secret = api_secret
        self.api_version = api_version

    def create_client_token(self):
        query, variables = self._create_client_token_query()
        data = self._send_request(query, variables)
        return data

    def charge_payment_method(self, payment_method_id: str, amount: float):
        query, variables = self._charge_payment_method_query(payment_method_id, amount)
        data = self._send_request(query, variables)
        return data

    def _create_client_token_query(self):
        query = """
        mutation ClientToken($input: CreateClientTokenInput) {
            createClientToken(input: $input) {
                clientToken
            }
        }
        """
        variables = {
            "input": {"clientToken": {"merchantAccountId": self.merchant_account_id}}
        }
        return query, variables

    def _charge_payment_method_query(self, payment_method_id: str, amount: float):
        query = """
        mutation Charge($input: ChargePaymentMethodInput!) {
            chargePaymentMethod(input: $input) {
                transaction {
                    id
                    status
                }
            }
        }
        """
        variables = {
            "input": {
                "paymentMethodId": payment_method_id,
                "transaction": {
                    "amount": amount,
                    "merchantAccountId": self.merchant_account_id,
                },
            }
        }
        return query, variables

    def _send_request(self, query: str, variables: dict, timeout=30) -> dict:
        api_secret_bytes = f"{self.api_key}:{self.api_secret}".encode("ascii")
        encoded_secret = base64.b64encode(api_secret_bytes)
        headers = {
            "Authorization": f"Basic {encoded_secret.decode('ascii')}",
            "Braintree-Version": self.api_version,
        }

        try:
            response = requests.post(
                self.url,
                json={"query": query, "variables": variables},
                timeout=timeout,
                headers=headers,
            )
        except requests.Timeout:
            raise payment_processor_exceptions.BraintreeClientException(
                f"{LOGGER_PREFIX} timeout={timeout} exceeded"
            )
        except Exception as e:
            raise payment_processor_exceptions.BraintreeClientException(
                f"{LOGGER_PREFIX} {e}"
            )

        if response.status_code != 200:
            raise payment_processor_exceptions.BraintreeClientException(
                f"{LOGGER_PREFIX} failed sending request, status code {response.status_code}"
            )

        return response.json()
