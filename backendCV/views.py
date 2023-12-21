from django.shortcuts import render
from rest_framework import generics, status
from backendCV.models import *
from backendCV.serializers import *     
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib.auth import authenticate
from rest_framework_simplejwt.views import TokenRefreshView
from django.db import transaction
from datetime import timedelta

#PackageItems
class PackageItemsListCreateView(generics.ListCreateAPIView):
    queryset = PackageItems.objects.all()
    serializer_class = PackageItemsSerializer
    permission_classes = [IsAuthenticated]
    
class PackageItemsDetailUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PackageItems.objects.all()
    serializer_class = PackageItemsSerializer
    permission_classes = [IsAuthenticated]

#Package
class PackagesListCreateView(generics.ListCreateAPIView):
    queryset = Packages.objects.all()
    serializer_class = PackagesSerializer
    permission_classes = [IsAuthenticated]
    
class PackagesDetailUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Packages.objects.all()
    serializer_class = ItemsSerializer
    permission_classes = [IsAuthenticated]

#Items
class ItemsListCreateView(generics.ListCreateAPIView):
    queryset = Items.objects.all()
    serializer_class = ItemsSerializer
    permission_classes = [IsAuthenticated]
    
class ItemsDetailUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Items.objects.all()
    serializer_class = ItemsSerializer
    permission_classes = [IsAuthenticated]

#Areas
class AreasListCreateView(generics.ListCreateAPIView):
    queryset = Areas.objects.all()
    serializer_class = AreasSerializer
    permission_classes = [IsAuthenticated]
    
class AreasDetailUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Areas.objects.all()
    serializer_class = AreasSerializer
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
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        proforma_data = request.data
        observations_data = proforma_data.pop('observations', [])
        packages_data = proforma_data.pop('package', [])
        personal_proyecto_data = proforma_data.pop('personal_proyecto', [])

        proforma_serializer = ProformaSerializer(data=proforma_data)
        proforma_serializer.is_valid(raise_exception=True)
        proforma_instance = proforma_serializer.save()

        observations_data = [{'proforma_id': proforma_instance.proforma_id, **obs_data} for obs_data in observations_data]

        observations_serializer = ObservationsSerializer(data=observations_data, many=True)
        observations_serializer.is_valid(raise_exception=True)
        observations_serializer.save()

        for package_data in packages_data:
            package_data['proforma_id'] = proforma_instance.proforma_id
            package_serializer = PackagesSerializer(data=package_data)
            package_serializer.is_valid(raise_exception=True)
            package_instance = package_serializer.save()

            package_items_data = package_data.pop('package_items', [])

            package_items_data = [{'package_id': package_instance.package_id, **pks_items_data} for pks_items_data in package_items_data]

            package_items_serializer = PackageItemsSerializer(data=package_items_data, many=True)
            package_items_serializer.is_valid(raise_exception=True)
            package_items_serializer.save()

        personal_proyecto_data = [{'proforma_id': proforma_instance.proforma_id, **prsnal_proyect_data} for prsnal_proyect_data in personal_proyecto_data]

        personal_proyecto_serializer = PersonalProyectoSerializer(data=personal_proyecto_data, many=True)
        personal_proyecto_serializer.is_valid(raise_exception=True)
        personal_proyecto_serializer.save()

        return Response(proforma_serializer.data, status=status.HTTP_201_CREATED)

    
class ProformaDetailUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Proforma.objects.all()
    serializer_class = ProformaSerializer
    permission_classes = [IsAuthenticated]   
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data

        # Add Observations
        observations = Observations.objects.filter(proforma_id=instance)
        packages = Packages.objects.filter(proforma_id=instance)
        personal_proyecto = PersonalProyecto.objects.filter(proforma_id=instance)
        areas = Areas.objects.all()

        # Serializers
        observations_data = ObservationsSerializer(observations, many=True).data
        packages_data = PackagesSerializer(packages, many=True).data
        personal_proyecto_data = PersonalProyectoSerializer(personal_proyecto, many=True).data
        areas_data = AreasSerializer(areas, many=True).data

        # RPT
        data['observations'] = observations_data
        data['packages'] = packages_data
        data['personal_proyecto'] = personal_proyecto_data
        data['areas'] = areas_data

        # Add position
        for employee_data in data['personal_proyecto']:
            employee_id = employee_data['employees_id']
            employee_instance = Employees.objects.get(pk=employee_id)
            position_data = PositionListSerializer(employee_instance.id_position).data
            employee_data['position'] = position_data

        # Add Areas
        for area_data in data['areas']:
            area_id = area_data['area_id']
            items = Items.objects.filter(area_id=area_id)
            items_data = ItemsSerializer(items, many=True).data

            # Add package_items
            for item_data in items_data:
                item_id = item_data['item_id']
                package_number = 0

                for packages in packages_data:
                    package_item = PackageItems.objects.filter(item_id=item_id, package_id=4)
                    package_items_data = PackageItemsSerializer(package_item, many=True).data
                    package_number = package_number + 1
                    item_data[f'package_{package_number}'] = package_items_data
                # Remove the line below if 'package_items' field is not present in item_data
                item_data.pop('package_items', None)

            area_data['items'] = items_data

        return Response(data)

    
#PersonalProyecto
class PersonalProyectoListCreateView(generics.ListCreateAPIView):
    queryset = PersonalProyecto.objects.all()
    serializer_class = PersonalProyectoSerializer
    permission_classes = [IsAuthenticated]
    
class PersonalProyectoDetailUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PersonalProyecto.objects.all()
    serializer_class = PersonalProyectoSerializer
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

#Employees
class EmployeesListCreateView(generics.ListCreateAPIView):
    queryset = Employees.objects.all()
    serializer_class = EmployeesSerializer
    permission_classes = [IsAuthenticated]
    
class EmployeesDetailUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employees.objects.all()
    serializer_class = EmployeesSerializer
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
            
            access_token = refresh.access_token
            access_token.set_exp(lifetime=timedelta(days=1))
            
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
                'access': str(access_token),
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
    
    
