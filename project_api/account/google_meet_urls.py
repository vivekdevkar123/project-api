from django.urls import path
from .views import google_meet_auth, google_meet_callback

urlpatterns = [
    path('auth/', google_meet_auth, name='google_meet_auth'),
    path('callback/', google_meet_callback, name='google_meet_callback'),
]
