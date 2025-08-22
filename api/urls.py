from django.urls import path
from .views import SendRentalConfirmationEmailView

urlpatterns = [
    path("send-confirmation-email/", SendRentalConfirmationEmailView.as_view(), name="send_confirmation_email"),
]
