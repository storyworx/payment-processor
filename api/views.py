import json
import logging

from rest_framework import status, views
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny  # , IsAuthenticated
from rest_framework.response import Response

from api import serializers
from payment_processor import constants as payment_processor_constants
from payment_processor import models as payment_proccessor_models
from payment_processor.processors import factory as payment_processor_factory

logger = logging.getLogger(__name__)


@permission_classes([AllowAny])
class PaymentRequestView(views.APIView):
    """Payment request endpoint"""

    serializer_class = serializers.PaymentRequestSerializer

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

        logger.info(f"Payment request submitted: {json.dumps(data, indent=2)}")

        user_id = data["buyer"]
        amount = data["base_amount"]
        token_code = data["quote_currency"]
        currency = data["base_currency"]
        payment_type = data["payment_type"]

        quote_amount = amount  # TODO: get amount from token service

        payment_service = payment_processor_factory.get_processor(payment_type)

        client_transaction_data = payment_service.init_payment(
            user_id=user_id,
            base_amount=amount,
            quote_amount=quote_amount,
            base_currency=currency,
            quote_currency=token_code,
            payment_type=payment_type,
            transaction_type=payment_processor_constants.TransactionType.BUY,
        )

        return Response(
            client_transaction_data,
            status=status.HTTP_200_OK,
        )

    def get(self, request):
        """Get payment requests"""
        models = payment_proccessor_models.Transaction.objects.all()
        serializer = self.serializer_class(models, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


@permission_classes([AllowAny])
class ProcessStripePaymentView(views.APIView):

    serializer_class = serializers.ProcessStripePaymentSerializer

    def post(self, request):

        external_id = (
            request.data.get("data", {}).get("object", {}).get("payment_intent")
        )
        transaction_status = (
            request.data.get("data", {}).get("object", {}).get("status")
        )

        request_data = {
            "external_id": external_id,
            "transaction_status": transaction_status,
        }

        serializer = self.serializer_class(
            context={"request": request}, data=request_data
        )

        if not serializer.is_valid():
            return Response(
                {"errors": [{"message": "Invalid POST body", "code": "BAD_REQUEST"}]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # data = serializer.validated_data

        # payment_type = payment_processor_constants.PaymentType.CREDIT_CARD
        # payment_service = payment_factory.PAYMENT_SERVICES[payment_type]()

        # payment_service.process_payment(user=None, txid=data["external_id"])
