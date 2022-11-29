from rest_framework import serializers


class PaymentRequestSerializer(serializers.Serializer):
    buyer = serializers.IntegerField(required=True)
    seller = serializers.IntegerField(default=None)
    payment_type = serializers.CharField(required=True)
    transaction_type = serializers.CharField(default=None)
    status = serializers.CharField(default=None)
    base_currency = serializers.CharField(required=True)
    quote_currency = serializers.CharField(required=True)
    base_amount = serializers.FloatField(required=True, min_value=0)

    class Meta:
        read_only_fields = ("seller", "transaction_type", "status")


class ProcessStripePaymentSerializer(serializers.Serializer):
    external_id = serializers.CharField(write_only=True, required=True)
    transaction_status = serializers.CharField(write_only=True, required=True)
