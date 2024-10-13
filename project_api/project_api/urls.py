# project_api/urls.py
from django.contrib import admin
from django.urls import path, include
from account.views import CreateGoogleMeetLinkView, GoogleMeetCallbackView  # Import your views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include('account.urls')),  # Includes user-related API endpoints
    path('api/create-meet/', CreateGoogleMeetLinkView.as_view(), name='create_meet'),  # Link to CreateGoogleMeetLinkView
    path('api/google-meet/callback/', GoogleMeetCallbackView.as_view(), name='google_meet_callback'),  # Link to GoogleMeetCallbackView
]
