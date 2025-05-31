from django.urls import path
from . import views

urlpatterns = [
    path('music/<str:pk>/', views.music, name='music'),
    path('fav_list/', views.fav_playlist, name='favourite'),
    path('fav/<str:pk>/', views.save_fav, name='save_fav'),
    path('search/', views.search, name='search'),
]