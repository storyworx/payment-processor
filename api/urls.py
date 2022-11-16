from django.urls import re_path

from api import views

urlpatterns = [
    re_path(
        r"^payment-request/?$",
        views.PaymentRequestView.as_view(),
        name="payment-request",
    ),
]
