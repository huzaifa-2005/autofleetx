from allauth.socialaccount.signals import pre_social_login
from django.dispatch import receiver
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(pre_social_login)
def link_to_existing_user(sender, request, sociallogin, **kwargs):
    """
    When a user logs in via Google and an account with the same email already exists,
    link the social account to the existing user instead of creating a duplicate.
    """
    email = sociallogin.account.extra_data.get('email')

    if not email:
        return  # No email — can't proceed

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return  # No matching user — continue default flow

    if not sociallogin.is_existing:
        sociallogin.connect(request, user)
