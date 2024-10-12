from django.urls import path
from account.views import (
    UserRegistrationView,
    UserLoginView,
    UserProfileView,
    UserChangePasswordView,
    SendPasswordResetEmailView,
    UserPasswordResetView,
    VerifyOtpView,
    SendOTPView
)
from . import views

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('verify-otp/', VerifyOtpView.as_view(), name='verify-otp'),
    path('send-otp/', SendOTPView.as_view(), name='send-otp'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('changepassword/', UserChangePasswordView.as_view(), name='changepassword'),
    path('send-reset-password-email/', SendPasswordResetEmailView.as_view(), name='send-reset-password-email'),
    path('reset-password/<uid>/<token>/', UserPasswordResetView.as_view(), name='reset-password'),
    path('google-meet/auth/', views.google_meet_auth, name='google_meet_auth'),
    path('google-meet/callback/', views.google_meet_callback, name='google_meet_callback'),
    path('api/create-google-meet/', views.create_google_meet, name='create-google-meet'),  # New endpoint for creating Google Meet
]
