from rest_framework import serializers


class PaymentRequestSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(write_only=True, required=True)
    payment_type = serializers.CharField(write_only=True, required=True)
    base_currency = serializers.CharField(write_only=True, required=True)
    quote_currency = serializers.CharField(write_only=True, required=True)
    amount = serializers.FloatField(write_only=True, required=True, min_value=0)


class ProcessStripePaymentSerializer(serializers.Serializer):
    external_id = serializers.CharField(write_only=True, required=True)
    transaction_status = serializers.CharField(write_only=True, required=True)
