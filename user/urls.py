from django.urls import path
from . import views


urlpatterns = [
    path('login_page/', views.login_view, name='login'),
    
]