from django.shortcuts import render
from rest_framework import generics, status
from backendCV.models import Employee, Company, User
from backendCV.serializers import EmployeeListSerializer, CompanyListSerializer, UserRegistrationSerializer, UserLoginSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

# Vista para el registro de usuarios
class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

# Vista para el login
class UserLoginView(generics.CreateAPIView):
    serializer_class = UserLoginSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')

        # Autenticar al usuario
        user = authenticate(request, username=username, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            # Obtener los datos del usuario
            user_data = {
                'id': user.id,
                'username': user.username,
                'nombre': user.nombre,
                'apellidos': user.apellidos,
                'email': user.email,
            }

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': user_data,
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)
        

class EmployeeList(generics.ListAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeListSerializer
    permission_classes = [IsAuthenticated]
    

class CompanyList(generics.ListAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanyListSerializer
    permission_classes = [IsAuthenticated]

    
