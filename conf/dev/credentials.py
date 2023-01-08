import functools
import json

import consul
from django.conf import settings
from dotenv import load_dotenv

c = consul.Consul(host=settings.HOST_IP)


def get_settings(prefix_path: str, key: str):
    _, data = c.kv.get(prefix_path)
    config = json.loads(data["Value"])
    path = key.split("/")
    return functools.reduce(
        lambda a, b: a.get(b) if isinstance(a, dict) else a, path, config
    )


# STRIPE
"""
prefix_path = payment-processor/stripe
{
    api_key: <value>,
    api_secret: <value>
}
"""


class StripeCredentials:
    PREFIX_PATH = "payment-processor/stripe"

    def __init__(self) -> None:
        self.STRIPE_API_KEY = get_settings(self.PREFIX_PATH, "api_key")
        self.STRIPE_API_SECRET = get_settings(self.PREFIX_PATH, "api_secret")


# BRAINTREE
"""
prefix_path = payment-processor/braintree
{
    url: <value>
    api_key: <value>,
    api_secret: <value>
    merchant_id: <value>
    merchant_account_ids: {
        USD: <value>
        EUR: <value>
        GBP: <value>
    }
}
"""


class BraintreeCredentials:
    PREFIX_PATH = "payment-processor/braintree"

    def __init__(self) -> None:
        self.API_KEY = get_settings(self.PREFIX_PATH, "api_key")
        self.API_SECRET = get_settings(self.PREFIX_PATH, "api_secret")
        self.API_VERSION = get_settings(self.PREFIX_PATH, "api_version")
        self.URL = get_settings(self.PREFIX_PATH, "url")
        self.MERCHANT_ID = get_settings(self.PREFIX_PATH, "merchant_id")
        self.MERCHANT_ACCOUNT_IDS = get_settings(
            self.PREFIX_PATH, f"merchant_account_ids"
        )
