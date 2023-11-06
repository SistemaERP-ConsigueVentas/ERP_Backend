from django.db import models

# Create your models here.
class User(models.Model):
    user_id = models.SmallAutoField(primary_key=True)
    nombre = models.CharField(max_length=20)
    apellidos = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    
    def __str__(self):
        return self.nombre