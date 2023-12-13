from django.shortcuts import render
from rest_framework import generics, status
from backendCV.models import *
from backendCV.serializers import *     
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib.auth import authenticate
from rest_framework_simplejwt.views import TokenRefreshView

#Payment Conditions
class PaymentConditionsListCreateView(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = PaymentConditionsSerializer
    permission_classes = [IsAuthenticated]
    
class PaymentConditionsDetailUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = PaymentConditionsSerializer
    permission_classes = [IsAuthenticated]

#Details Service
class DetailsServiceListCreateView(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = DetailsServiceSerializer
    permission_classes = [IsAuthenticated]
    
class DetailsServiceDetailUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = DetailsServiceSerializer
    permission_classes = [IsAuthenticated]

#Characteristics
class CharacteristicsListCreateView(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CharacteristicsSerializer
    permission_classes = [IsAuthenticated]
    
class CharacteristicsDetailUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CharacteristicsSerializer
    permission_classes = [IsAuthenticated]

#Company
class CompanyListCreateView(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]
    
class CompanyDetailUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]

#Proforma
class ProformaListCreateView(generics.ListCreateAPIView):
    serializer_class = ProformaSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Obtener el name de Company
        company_name = self.request.query_params.get('companyname', None)

        # Filtra las Proformas por nombre de la Company si el parámetro está presente
        if company_name:
            queryset = Proforma.objects.filter(company_id__business_name__icontains=company_name)
        else:
            queryset = Proforma.objects.all()

        return queryset
    
    
class ProformaDetailUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Proforma.objects.all()
    serializer_class = ProformaSerializer
    permission_classes = [IsAuthenticated]

#Project
class ProjectListCreateView(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]
    
class ProjectDetailUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

#Observations
class ObservationsListCreateView(generics.ListCreateAPIView):
    queryset = Observations.objects.all()
    serializer_class = ObservationsSerializer
    permission_classes = [IsAuthenticated]
    
class ObservationsDetailUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Observations.objects.all()
    serializer_class = ObservationsSerializer
    permission_classes = [IsAuthenticated]

#Price
class PriceListCreateView(generics.ListCreateAPIView):
    queryset = Price.objects.all()
    serializer_class = PriceSerializer
    permission_classes = [IsAuthenticated]
    
class PriceDetailUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Price.objects.all()
    serializer_class = PriceSerializer
    permission_classes = [IsAuthenticated]

#Expense
class ExpenseListCreateView(generics.ListCreateAPIView):
    serializer_class = ExpenseSerializer

    def get_queryset(self):
        return Expense.objects.select_related('status_id')

    def list(self, request):
        expenses = self.get_queryset()

        # Filtrar gastos por estado y organizar en 4 listas
        status_lists = {
            'Aprobado': [],
            'Rechazado': [],
            'Por aprobar': [],
            'Por enviar': [],
        }

        for expense in expenses:
            status_label = expense.status_id.name
            status_lists[status_label].append(ExpenseSerializer(expense).data)

        return Response(status_lists)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ExpenseDetailUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def patch(self, request, **kwargs):
        expense = self.get_object()

        # verificar si existe "new_status_id" en la Url
        new_status_id = kwargs.get('new_status_id', None)

        if new_status_id:
            # Llamar al método para cambiar el estado
            return self.status_change(expense, new_status_id)

        serializer = self.get_serializer(expense, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def status_change(self, expense, new_status_id):
        # Estados en BD IDs:
        # Aprobado = 1,
        # Rechazado = 2,
        # Por aprobar = 3,
        # Por enviar = 4,
        current_status_id = expense.status_id_id

        # Validaciones
        if current_status_id == 4 and new_status_id == 3:
            # Cambiar de 'Por enviar' a 'Por aprobar' es válido
            pass
        elif current_status_id == 3 and new_status_id in [1, 2]:
            # Cambiar de 'Por aprobar' a 'Aceptado' o 'Rechazado' es válido
            pass
        else:
            return Response({'error': 'Cambio de estado no permitido'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            new_status = ExpenseStatus.objects.get(pk=new_status_id)
        except ExpenseStatus.DoesNotExist:
            return Response({'error': f'El estado con ID "{new_status_id}" no existe'}, status=status.HTTP_404_NOT_FOUND)

        expense.status_id = new_status
        expense.save()

        serializer = self.get_serializer(expense)
        return Response(serializer.data)
    
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

#Vista para el Refresh Token
class RefreshTokenView(TokenRefreshView):
    def post(self, request):
        refresh_token = request.headers.get('Authorization', '').split(' ')[-1]

        serializer = self.get_serializer(data={'refresh': refresh_token})

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            return Response({'error': 'Token de actualización no válido'}, status=401)

        return Response({
            'access': str(serializer.validated_data['access']),
        }) 
        
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
    
    
