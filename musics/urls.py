from django.urls import path
from . import views

urlpatterns = [
    path('music/<str:pk>/', views.music, name='music'),
]