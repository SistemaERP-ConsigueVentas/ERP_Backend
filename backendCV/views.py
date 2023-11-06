from django.shortcuts import render
from rest_framework import generics, status
from backendCV.models import User
from backendCV.serializers import UserListSerializer

# Create your views here.

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
