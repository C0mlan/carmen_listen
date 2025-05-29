
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('rest_framework.urls')),
    path('user/', include("user.urls")),
    path('musics/', include("musics.urls")),
]
