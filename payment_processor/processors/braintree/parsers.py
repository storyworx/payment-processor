def parse_client_token(data: dict) -> str:
    return data.get("data", {}).get("createClientToken", {}).get("clientToken", None)


def parse_transaction_id(data: dict) -> str:
    return (
        data.get("data", {})
        .get("chargePaymentMethod", {})
        .get("transaction", {})
        .get("id", None)
    )


def parse_transaction_status(data: dict) -> str:
    return (
        data.get("data", {})
        .get("chargePaymentMethod", {})
        .get("transaction", {})
        .get("status", None)
    )
