import json
import logging

from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from api import serializers
from payment_processor import constants as payment_processor_constants
from payment_processor import models as payment_proccessor_models
from payment_processor.processors import factory as payment_processor_factory

logger = logging.getLogger(__name__)

LOGGER_PREFIX = "[API-VIEW]"


@permission_classes([AllowAny])
class PaymentRequestView(generics.ListAPIView):
    """Payment request endpoint"""

    queryset = payment_proccessor_models.Transaction.objects.all()
    serializer_class = serializers.PaymentRequestSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        "buyer": ["exact"],
        "seller": ["exact"],
        "payment_type": ["exact"],
        "transaction_type": ["exact"],
        "status": ["exact"],
        "base_currency": ["exact"],
        "quote_currency": ["exact"],
        "base_amount": ["lte", "gte"],
        "quote_amount": ["lte", "gte"],
        "date_created": ["lte", "gte"],
        "date_changed": ["lte", "gte"],
    }

    @extend_schema(operation_id="Initialize Payment request", tags=["PaymentRequest"])
    def post(self, request):
        """Send 'transfer_amount' of tokens to user with id='source_pk'."""

        serializer = self.serializer_class(
            context={"request": request}, data=request.data
        )

        if not serializer.is_valid():
            return Response(
                {"errors": [{"message": "Invalid POST body", "code": "BAD_REQUEST"}]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        data = serializer.validated_data

        logger.info(
            f"{LOGGER_PREFIX} Payment request submitted: {json.dumps(data, indent=2)}"
        )

        user_id = data["buyer"]
        amount = data["base_amount"]
        token_code = data["quote_currency"]
        currency = data["base_currency"]
        payment_type = data["payment_type"]

        quote_amount = amount  # TODO: get amount from token service

        payment_service = payment_processor_factory.get_processor(payment_type)

        init_payment_params = {
            "user_id": user_id,
            "base_amount": amount,
            "quote_amount": quote_amount,
            "base_currency": currency,
            "quote_currency": token_code,
            "payment_type": payment_type,
            "transaction_type": payment_processor_constants.TransactionType.MINT,
        }

        if payment_type == payment_processor_constants.PaymentType.PAYPAL.value:
            init_payment_params["payment_method_id"] = data["extras"][
                "payment_method_id"
            ]

        client_transaction_data = payment_service.init_payment(**init_payment_params)

        if payment_type == payment_processor_constants.PaymentType.PAYPAL.value:
            payment_service.process_payment(
                client_transaction_data["txid"], client_transaction_data["status"]
            )
            client_transaction_data = {"status": "ok"}

        return Response(
            client_transaction_data,
            status=status.HTTP_200_OK,
        )

    @extend_schema(operation_id="List all Payment requests", tags=["PaymentRequest"])
    def get(self, request):
        """Get payment requests"""
        return super().list(request)


@permission_classes([AllowAny])
class BraintreeClientToken(generics.GenericAPIView):
    serializer_class = serializers.BraintreeClientTokenSerializer

    @extend_schema(operation_id="Get Braintree client token", tags=["Braintree"])
    def get(self, request):
        payment_service = payment_processor_factory.get_processor(
            payment_processor_constants.PaymentType.PAYPAL.value
        )

        data = payment_service.create_client_token()

        return Response(
            data,
            status=status.HTTP_200_OK,
        )
