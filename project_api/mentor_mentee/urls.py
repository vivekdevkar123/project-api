from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_participant, name='create_participant'),
    path('list_participants/', views.list_participants, name='list_participants'),
    path('linkedin/post/', views.linkedin_post, name='linkedin_post'),
]
