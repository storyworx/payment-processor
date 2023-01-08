from rest_framework import serializers

from payment_processor import constants


class PaymentRequestSerializer(serializers.Serializer):
    txid = serializers.UUIDField(default=None, required=False, read_only=True)
    buyer = serializers.IntegerField(required=True)
    seller = serializers.IntegerField(default=None, required=False, read_only=True)
    payment_type = serializers.ChoiceField(
        required=True, choices=constants.PaymentType.choices()
    )
    transaction_type = serializers.ChoiceField(
        default=None,
        required=False,
        read_only=True,
        choices=constants.TransactionType.choices(),
    )
    status = serializers.ChoiceField(
        default=None,
        required=False,
        read_only=True,
        choices=constants.TransactionStatus.choices(),
    )
    base_currency = serializers.CharField(required=True)
    quote_currency = serializers.CharField(required=True)
    base_amount = serializers.FloatField(required=True, min_value=0)
    quote_amount = serializers.FloatField(required=False, read_only=True)
    date_created = serializers.DateTimeField(required=False, read_only=True)
    date_changed = serializers.DateTimeField(required=False, read_only=True)
    extras = serializers.DictField(required=False, write_only=True)


class BraintreeClientTokenSerializer(serializers.Serializer):
    client_token = serializers.CharField(required=False, read_only=True)
