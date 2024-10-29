from django.urls import path
from projectUtility.views import LinkedInAuthView,IndexView,AuthorizeView,CallbackView,CheckAuthView,CreateMeetView

urlpatterns = [
    path('google-meet-home/', IndexView.as_view(), name='google-meet-home'),
    path('authorize/', AuthorizeView.as_view(), name='authorize'),
    path('callback/', CallbackView.as_view(), name='callback'),
    path('check-auth/', CheckAuthView.as_view(), name='check_auth'),
    path('create-meet', CreateMeetView.as_view(), name='create_meet'),
    path('linkedin-auth/', LinkedInAuthView.as_view(),name='linkedin-authentication'),
]