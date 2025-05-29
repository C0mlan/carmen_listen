from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


# Create your views here.
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username= request.data.get("username")
    password = request.data.get("password")
    user = authenticate(username=username, password=password)
  
    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
            "token_type": "bearer"
            }, status=status.HTTP_200_OK)
      
    return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)