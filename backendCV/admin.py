from django.contrib import admin
from backendCV.models import User, Core, Department, Position

# Register your models here.
admin.site.register(User)
admin.site.register(Position)
admin.site.register(Core)
admin.site.register(Department)
