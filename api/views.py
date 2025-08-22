from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site

User = get_user_model()

class SendRentalConfirmationEmailView(APIView):
    
    def post(self, request):
        user_id = request.data.get("user_id")
        car_name = request.data.get("car_name")
        rental_days = request.data.get("rental_days")
        rental_minutes = request.data.get("rental_minutes")
        total_cost = request.data.get("total_cost")
        current_site = get_current_site(request)
        home_url = f"http://{current_site.domain}{reverse('home')}"  

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # Prepare HTML email content
        subject = "Car Rental Confirmation"
        from_email = settings.DEFAULT_FROM_EMAIL
        if not user.email:
            return Response({"error": "User does not have an email address"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            to_email = [user.email]

        html_content = render_to_string("emails/rental_confirmation.html", {
            "user": user,
            "car_name": car_name,
            "rental_days": rental_days,
            "rental_minutes": rental_minutes,
            "total_cost": total_cost,
            "home_url": home_url,
        })
        text_content = f"Hello {user.username},\n\nYour rental for {car_name} has been confirmed."

        email = EmailMultiAlternatives(subject, text_content, from_email, to_email)
        email.attach_alternative(html_content, "text/html")
        email.send()

        return Response({"message": "Email sent successfully"}, status=status.HTTP_200_OK)

