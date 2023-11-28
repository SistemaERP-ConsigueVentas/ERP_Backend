from django.shortcuts import render
from rest_framework import generics, status
from backendCV.models import Client, Invoice, User, Department, Core, Position
from backendCV.serializers import ClientSerializer, InvoiceSerializer, UserRegistrationSerializer, UserLoginSerializer, ChangePasswordSerializer, UserListSerializer, CoreListSerializer, PositionListSerializer, DepartmentListSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

# Cliente
class ClientListCreateView(generics.ListCreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]

class ClientUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]

# Factura
class InvoiceListCreateView(generics.ListCreateAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated]

class InvoiceUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated]

class InvoiceSearchByClientView(generics.ListAPIView):
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        client_id = self.kwargs['client_id']
        # Relación a través de las claves foráneas en modelo Sale
        return Invoice.objects.filter(sale__client_id=client_id)

# Vista para el registro de usuarios
class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

    def perform_create(self, serializer):
        # Si es un superusuario, establecer el campo role en None
        if self.request.user.is_superuser:
            serializer.save(role=None)
        else:
            serializer.save()

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
        
# Vista para el cambio de contraseña
class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Obtener el usuario autenticado
        user = self.request.user

        # Verificar la antigua contraseña
        if not user.check_password(serializer.validated_data.get('old_password')):
            return Response({'error': 'La antigua contraseña no es válida.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Verificar que la nueva contraseña no sea igual a la antigua
        if serializer.validated_data.get('old_password') == serializer.validated_data.get('new_password'):
            return Response({'error': 'La nueva contraseña debe ser diferente de la antigua'}, status=status.HTTP_400_BAD_REQUEST)

        # Cambiar la contraseña
        user.set_password(serializer.validated_data.get('new_password'))
        user.save()

        return Response({'message': 'Contraseña cambiada exitosamente.'}, status=status.HTTP_200_OK)
    
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [IsAuthenticated]
    
class UserForId(generics.RetrieveAPIView):
    serializer_class = UserListSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'
    
class CoreList(generics.ListAPIView):
    queryset = Core.objects.all()
    serializer_class = CoreListSerializer
    permission_classes = [IsAuthenticated]
    
class DepartmentList(generics.ListAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentListSerializer
    permission_classes = [IsAuthenticated]

class PositionList(generics.ListAPIView):
    queryset = Position.objects.all()
    serializer_class = PositionListSerializer
    permission_classes = [IsAuthenticated]
    
    
