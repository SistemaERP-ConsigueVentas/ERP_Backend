from django.shortcuts import render
from rest_framework import generics, status
from backendCV.models import Employee, Company, User
from backendCV.serializers import EmployeeListSerializer, CompanyListSerializer, UserRegistrationSerializer, UserLoginSerializer
from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer


class UserLoginView(generics.CreateAPIView):
    serializer_class = UserLoginSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        username = serializer.validated_data.get('username')
        user = User.objects.get(username=username)  # Buscar el usuario por nombre de usuario
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)
        

class EmployeeList(generics.ListAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeListSerializer
    permission_classes = [IsAuthenticated]
    

class CompanyList(generics.ListAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanyListSerializer
    permission_classes = [IsAuthenticated]

    
