from rest_framework import generics, status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response

# from api import serializers

# from payment_processor import constants as payment_processor_constants


@permission_classes([AllowAny])
class ApiDocs(generics.GenericAPIView):
    """Send 'transfer_amount' of tokens to user with id='source_pk'."""

    renderer_classes = [TemplateHTMLRenderer]
    serializer_class = None

    def get(self, request):
        return Response(template_name="api-docs.html")


@permission_classes([AllowAny])
class Healthcheck(generics.GenericAPIView):
    """Healthcheck endpoint"""

    serializer_class = None

    def get(self, request):
        return Response(
            status=status.HTTP_200_OK,
        )
