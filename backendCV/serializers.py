from rest_framework import serializers
from backendCV.models import User, Department, Core, Position

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

# Serializer para el modelo Position
class PositionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = '__all__' # Incluye todos los campos del modelo Company
    
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
