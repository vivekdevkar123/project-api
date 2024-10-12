from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_participant, name='create_participant'),
    path('list_participants/', views.list_participants, name='list_participants'),
]
