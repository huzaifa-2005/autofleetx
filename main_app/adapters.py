from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from allauth.exceptions import ImmediateHttpResponse
from django.conf import settings

User = get_user_model()

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    """
    When a social login comes in, if the social account is not already
    linked (sociallogin.is_existing is False) but the social account's
    email matches an existing user.email, link it to that user and
    immediately redirect (so no signup form appears).
    """

    def pre_social_login(self, request, sociallogin):
        # If it's already linked to a user, do nothing
        if sociallogin.is_existing:
            return

        # Try to get an email from the sociallogin payload
        email = None
        # most providers put email in account.extra_data
        if hasattr(sociallogin, "account") and sociallogin.account:
            email = sociallogin.account.extra_data.get("email")
        # fallback to sociallogin.user.email (sometimes populated earlier)
        if not email:
            email = getattr(sociallogin.user, "email", None)

        if not email:
            # Nothing to match on; let default flow continue
            return

        # Case-insensitive match on email
        try:
            existing = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            return

        # Connect the social account to the existing user
        # This will create a SocialAccount entry linked to existing user
        sociallogin.connect(request, existing)

        # Immediately returning a redirect response so allauth doesn't continue to signup form.
        # Redirect target: LOGIN_REDIRECT_URL or home
        redirect_to = getattr(settings, "LOGIN_REDIRECT_URL", "/")
        raise ImmediateHttpResponse(redirect(redirect_to))
