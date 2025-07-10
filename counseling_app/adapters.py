from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings
from django.contrib.auth import login
from .models import AdminUser  # Ensure AdminUser is imported

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        user_email = sociallogin.user.email
        if user_email:
            try:
                # Check if an AdminUser with this email already exists
                existing_user = AdminUser.objects.get(email=user_email)
                # Automatically log in the user if they already exist
                login(request, existing_user, backend='allauth.account.auth_backends.AuthenticationBackend')
                raise ImmediateHttpResponse(redirect(settings.LOGIN_REDIRECT_URL))
            except AdminUser.DoesNotExist:
                # If the email does not exist in AdminUser, prevent login
                raise ImmediateHttpResponse(redirect(reverse('admin_login') + '?error=unauthorized_email'))

    def get_user_for_social_login(self, request, sociallogin):
        # Try to find an existing AdminUser with the same email
        try:
            return AdminUser.objects.get(email=sociallogin.user.email)
        except AdminUser.DoesNotExist:
            return None

    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        # Check if an AdminUser with this email already exists
        try:
            existing_admin_user = AdminUser.objects.get(email=user.email)
            # If an existing AdminUser is found, use that one
            sociallogin.user = existing_admin_user
            user = existing_admin_user
        except AdminUser.DoesNotExist:
            pass # No existing AdminUser, proceed with default allauth user creation/linking

        return user
