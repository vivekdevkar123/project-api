from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include('account.urls')),  # Existing user URLs
    path('google-meet/', include('account.google_meet_urls')),   
]
