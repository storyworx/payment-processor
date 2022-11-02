from rest_framework import status, views
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from api import serializers

# from payment_processor import constants as payment_processor_constants


@permission_classes([IsAuthenticated])
class PaymentRequestView(views.APIView):
    """Send 'transfer_amount' of tokens to user with id='source_pk'."""

    serializer_class = serializers.PaymentRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(
            context={"request": request}, data=request.data
        )

        if not serializer.is_valid():
            return Response(
                {"errors": [{"message": "Invalid POST body", "code": "BAD_REQUEST"}]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # data = serializer.validated_data

        # user = data["user_id"]
        # payment_type = payment_processor_constants.PaymentType[data["payment_type"]]
        # amount = data["amount"]
        # token_code = data["quote_currency"]
        # currency = data["base_currency"]

        # token = Token.objects.get(token_code=token_code)
        # quote_amount = amount / token.price

        # payment_service = payment_factory.PAYMENT_SERVICES[payment_type]()

        # client_transaction_data = payment_service.init_payment(
        #     user=user,
        #     base_amount=amount,
        #     quote_amount=quote_amount,
        #     base_currency=currency,
        #     quote_currency=token_code,
        #     payment_type=payment_type,
        #     transaction_type=payment_processor_constants.TransactionType.BUY,
        # )

        # return Response(
        #     client_transaction_data,
        #     status=status.HTTP_200_OK,
        # )


@permission_classes([AllowAny])
class ProcessStripePaymentView(views.APIView):
    """Send 'transfer_amount' of tokens to user with id='source_pk'."""

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