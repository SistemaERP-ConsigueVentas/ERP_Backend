from rest_framework import serializers
from backendCV.models import * 

# Serializer para el modelo Items
class ItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Items
        fields = '__all__'

# Serializer para el modelo PackageItems
class PackageItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageItems
        fields = '__all__'

# Serializer para el modelo Company
class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


# Serializer para el modelo Areas
class AreasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Areas
        fields = '__all__'

# Serializer para el modelo Observations
class ObservationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Observations
        fields = '__all__'
        
# Serializer para el modelo Proforma
class ProformaSerializer(serializers.ModelSerializer):
    company = CompanySerializer(source='company_id', read_only=True)
    class Meta:
        model = Proforma
        fields = '__all__'

# Serializer para el modelo Packages
class PackagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Packages
        fields = '__all__'


# Serializer para el modelo Position
class PositionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = '__all__' # Incluye todos los campos del modelo Company

# Serializer para el modelo Employees
class EmployeesSerializer(serializers.ModelSerializer):
    position = PositionListSerializer(source='id_position', read_only=True)
    class Meta:
        model = Employees
        fields = '__all__'

# Serializer para el modelo PersonalProyecto
class PersonalProyectoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalProyecto
        fields = '__all__'

# Serializer para el modelo Expenses_Status
class ExpenseStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseStatus
        fields = '__all__'
        
# Serializer para el modelo Expenses
class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'

# Serializer para el modelo Client
class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'
# Serializer para el modelo Invoice
class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'

# Serializer para el modelo Department
class DepartmentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__' # Incluye todos los campos del modelo Company

# Serializer para el modelo Core
class CoreListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Core
        fields = '__all__' # Incluye todos los campos del modelo Core

    
# Serializer para el modelo User (para registro)
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'nombre', 'apellidos', 'email', 'username', 'password', 'position_id']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

# Serializer para el modelo User (para login)
class UserLoginSerializer(serializers.Serializer):
    # Especifica los campos requeridos para la autenticación
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
# Serializer para cambio de contraseña
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

# Serializer para el modelo User (List User)
class UserListSerializer(serializers.ModelSerializer):
    position_name = serializers.CharField(source='position_id', read_only=True)
    core_name = serializers.CharField(source='position_id.cores_id', read_only=True)
    department_name = serializers.CharField(source='position_id.department_id', read_only=True)
    
    class Meta:
        model = User
        fields = ['id','email','nombre','apellidos','username','position_name', 'core_name', 'department_name']
