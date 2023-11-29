from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

#Modelo Expenses_Status
class Expense_Status(models.Model):
    id_status = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    
    def __str__(self):
            return self.name

#Modelo Expenses
class Expense(models.Model):
    id_expense = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    made_by = models.CharField(max_length=40)
    # Clave foránea que establece una relación con el modelo Expense_Status
    status_id = models.ForeignKey(Expense_Status, on_delete=models.CASCADE)
    
    def __str__(self):
            return self.name
        
#Modelo Clients
class Client(models.Model):
    id_client = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40)
    surname = models.CharField(max_length=40)
    email = models.EmailField(unique=True)
    cell = models.CharField(max_length=9)
    
    def __str__(self):
        return self.name

#Modelo Invoices
class Invoice(models.Model):
    id = models.AutoField(primary_key=True)
    serie = models.CharField(max_length=10)
    number = models.PositiveIntegerField()
    ruc = models.CharField(max_length=13)
    business_name = models.CharField(max_length=255)
    address = models.TextField()
    description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    money = models.CharField(max_length=3)
    status = models.BooleanField(default=False)
    date_of_issue = models.DateField()

    def __str__(self):
        return str(self.number)

#Modelo Sales
class Sale(models.Model):
    id_sale = models.AutoField(primary_key=True)
    date = models.DateField()
    product = models.CharField(max_length=255)
    
    # Clave foránea que establece una relación con el modelo Clients
    client_id = models.ForeignKey(Client, on_delete=models.CASCADE)
    # Clave foránea que establece una relación con el modelo Invoices
    invoice_id = models.ForeignKey(Invoice, on_delete=models.CASCADE)

    def __str__(self):
        return self.product

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

