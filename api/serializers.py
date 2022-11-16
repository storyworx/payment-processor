from rest_framework import serializers


class PaymentRequestSerializer(serializers.Serializer):
    buyer = serializers.IntegerField(required=True)
    seller = serializers.IntegerField(required=True)
    payment_type = serializers.CharField(required=True)
    transaction_type = serializers.CharField(required=True)
    status = serializers.CharField(required=True)
    base_currency = serializers.CharField(required=True)
    quote_currency = serializers.CharField(required=True)
    base_amount = serializers.FloatField(required=True, min_value=0)

    class Meta:
        read_only_fields = ("seller", "transaction_type", "status")


class ProcessStripePaymentSerializer(serializers.Serializer):
    external_id = serializers.CharField(write_only=True, required=True)
    transaction_status = serializers.CharField(write_only=True, required=True)
