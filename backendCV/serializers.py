from rest_framework import serializers
from backendCV.models import Employee, Company

# Serializer CompanyListSerializer para el modelo Company
class CompanyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__' # Incluye todos los campos del modelo Company


# Serializer UserListSerializer para el modelo User
class EmployeeListSerializer(serializers.ModelSerializer):
    
    company_name = serializers.CharField(source='company_id.name', read_only=True)
    
    class Meta:
        model = Employee
        fields = ['user_id','nombre','apellidos','email','company_id','company_name']