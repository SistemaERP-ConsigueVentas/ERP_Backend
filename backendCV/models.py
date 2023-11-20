from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

#Modelo Department
class Department(models.Model):
    id_department = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40)
    
    def __str__(self):
        return self.name

#Modelo Core
class Core(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40)
    
    # Clave foránea que establece una relación con el modelo Department
    department_id = models.ForeignKey(Department, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

#Modelo Position
class Position(models.Model):
    id_position = models.AutoField(primary_key=True)
    name = models.CharField(max_length=60)
    
    # Clave foránea que establece una relación con el modelo Department y Core
    department_id = models.ForeignKey(Department, on_delete=models.CASCADE)
    cores_id = models.ForeignKey(Core, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
#Gestor de usuarios personalizado
class UserManager(BaseUserManager):
    # Método para crear un usuario regular
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('El campo username es obligatorio.')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    # Método para crear un superusuario
    def create_superuser(self, username, password=None, **extra_fields):
        # Configuración predeterminada para un superusuario
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)

# Modelo de Usuario personalizado
class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    nombre = models.CharField(max_length=30)
    apellidos = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=100)
    
    # Clave foránea que establece una relación con el modelo Position
    position_id = models.ForeignKey(Position, on_delete=models.CASCADE)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['nombre', 'apellidos', 'position_id']

    def __str__(self):
        return self.nombre

