# Generated by Django 4.2.7 on 2023-11-29 17:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backendCV', '0014_expense_status_expense'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Expense_Status',
            new_name='ExpenseStatus',
        ),
    ]
