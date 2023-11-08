from django.db import models

# Create your models here.

#Modelo Company
class Company(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    
    def __str__(self):
        return self.name

#Modelo Employee
class Employee(models.Model):
    user_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=20)
    apellidos = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    
    # Clave foránea que establece una relación con el modelo Company
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE, default=1)
    
    def __str__(self):
        return self.nombre
    
    

    