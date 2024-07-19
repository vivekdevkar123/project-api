from django.urls import path
from account.views import UserRegistrationView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(),name='register'),
]