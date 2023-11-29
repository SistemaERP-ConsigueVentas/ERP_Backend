from django.contrib import admin
from backendCV.models import User, Core, Department, Position, Client, Invoice, Sale, ExpenseStatus, Expense

# Register your models here.
admin.site.register(User)
admin.site.register(Position)
admin.site.register(Core)
admin.site.register(Department)
admin.site.register(Client)
admin.site.register(Invoice)
admin.site.register(Sale)
admin.site.register(ExpenseStatus)
admin.site.register(Expense)
