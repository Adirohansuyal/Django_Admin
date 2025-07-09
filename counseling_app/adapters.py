from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings
from .models import AdminUser

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        user_email = sociallogin.user.email
        if user_email:
            # Check if the email is in the authorized list
            if user_email not in settings.AUTHORIZED_ADMIN_EMAILS:
                raise ImmediateHttpResponse(redirect(reverse('admin_login') + '?error=unauthorized_google_email'))

            try:
                # Check if an AdminUser with this email already exists
                AdminUser.objects.get(email=user_email)
            except AdminUser.DoesNotExist:
                # If the email does not exist in AdminUser, prevent login
                raise ImmediateHttpResponse(redirect(reverse('admin_login') + '?error=unauthorized_email'))
