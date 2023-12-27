from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

#Modelo Company
class Company(models.Model):
    company_id = models.AutoField(primary_key=True)
    business_name = models.CharField(max_length=255)
    tax_id = models.CharField(max_length=15)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(max_length=255)
    website = models.CharField(max_length=50)
    office_address = models.CharField(max_length=255)
    category = models.CharField(max_length=50)
    
    def __str__(self):
        return self.business_name
    
#Modelo Proforma
class Proforma(models.Model):
    proforma_id = models.AutoField(primary_key=True)
    invoice_number = models.CharField(max_length=20)
    date = models.DateField()
    reference = models.CharField(max_length=255)
    prepared_by = models.CharField(max_length=255)
    approved_by = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    work_time = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    required_by = models.CharField(max_length=255)

     # Clave foránea que establece una relación con el modelo Company 
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.invoice_number

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

#Modelo Employees 
class Employees(models.Model):
    employee_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    dni = models.CharField(max_length=12)
    cellphone = models.CharField
    
    # Clave foránea que establece una relación con el modelo Position
    id_position = models.ForeignKey(Position, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

#Modelo Proforma_Employees 
class PersonalProyecto(models.Model):
    # Clave foránea que establece una relación con el modelo Proforma
    proforma_id = models.ForeignKey(Proforma, on_delete=models.CASCADE)
    
    # Clave foránea que establece una relación con el modelo Employees
    employees_id = models.ForeignKey(Employees, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.employees_id)    

#Modelo class Observations
class Observations(models.Model):
    observation_id = models.AutoField(primary_key=True)
    description = models.TextField()
    
    # Clave foránea que establece una relación con el modelo Proforma
    proforma_id = models.ForeignKey(Proforma, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.observation_id)
    
#Modelo Packages
class Packages (models.Model):
    package_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    note_price = models.CharField(max_length=255)
    # Clave foránea que establece una relación con el modelo Proforma
    proforma_id = models.ForeignKey(Proforma, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
#Modelo Areas 
class Areas(models.Model):
    area_id = models.AutoField(primary_key=True)
    name  = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name       
    
#Modelo Items 
class Items(models.Model):
    item_id = models.AutoField(primary_key=True)
    detail  = models.CharField(max_length=50)
    description  = models.TextField()

    # Clave foránea que establece una relación con el modelo Area
    area_id = models.ForeignKey(Areas, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

#Modelo Package_Items 
class PackageItems(models.Model):
    value = models.CharField(max_length=255)
    # Clave foránea que establece una relación con el modelo Packages
    package_id = models.ForeignKey(Packages, on_delete=models.CASCADE)
    
    # Clave foránea que establece una relación con el modelo Items
    item_id = models.ForeignKey(Items, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.value

#Modelo Expenses_Status
class ExpenseStatus(models.Model):
    id_status = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    
    def __str__(self):
            return self.name

#Modelo Expenses
class Expense(models.Model):
    id_expense = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    made_by = models.CharField(max_length=40)
    # Clave foránea que establece una relación con el modelo Expense_Status
    status_id = models.ForeignKey(ExpenseStatus, on_delete=models.CASCADE)
    
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
    status = models.CharField(max_length=20)
    date_of_issue = models.DateField()

    # Clave foránea que establece una relación con el modelo Clients
    client_id = models.ForeignKey(Client, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.number)

#Modelo Sales
# class Sale(models.Model):
#     id_sale = models.AutoField(primary_key=True)
#     date = models.DateField()
#     product = models.CharField(max_length=255)
    
#     # Clave foránea que establece una relación con el modelo Clients
#     client_id = models.ForeignKey(Client, on_delete=models.CASCADE)
#     # Clave foránea que establece una relación con el modelo Invoices
#     invoice_id = models.ForeignKey(Invoice, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.product
    
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

