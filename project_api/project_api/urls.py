from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/',include('account.urls')),
    path('api/mentor_mentee/',include('mentor_mentee.urls')),
    path('api/utility/',include('projectUtility.urls')),
]
