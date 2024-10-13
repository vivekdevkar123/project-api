from django.urls import path
from .views import (
    UserRegistrationView,
    SendOTPView,
    VerifyOtpView,
    UserLoginView,
    UserProfileView,
    UserChangePasswordView,
    SendPasswordResetEmailView,
    UserPasswordResetView,
    CreateGoogleMeetLinkView,
    GoogleMeetCallbackView
)

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('send-otp/', SendOTPView.as_view(), name='send-otp'),
    path('verify-otp/', VerifyOtpView.as_view(), name='verify-otp'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('change-password/', UserChangePasswordView.as_view(), name='change-password'),
    path('send-reset-email/', SendPasswordResetEmailView.as_view(), name='send-reset-email'),
    path('reset-password/<uid>/<token>/', UserPasswordResetView.as_view(), name='reset-password'),
    path('create-meet/', CreateGoogleMeetLinkView.as_view(), name='create-meet'),
    path('google-meet/callback/', GoogleMeetCallbackView.as_view(), name='google-meet-callback'),
]
