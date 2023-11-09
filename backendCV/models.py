from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El campo Email es obligatorio.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    nombre = models.CharField(max_length=20)
    apellidos = models.CharField(max_length=50)
    username = models.CharField(max_length=50, default='hola', unique=True)
    password = models.CharField(max_length=100)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['nombre', 'apellidos']

    def __str__(self):
        return self.nombre


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
    
# class User(models.Model):
#     id = models.AutoField(primary_key=True)
#     nombre = models.CharField(max_length=20)
#     apellidos = models.CharField(max_length=50)
#     email = models.CharField(max_length=50)
#     username = models.CharField(max_length=50, default='hola')
#     password = models.CharField(max_length=100)
    
#     def __str__(self):
#         return self.nombre