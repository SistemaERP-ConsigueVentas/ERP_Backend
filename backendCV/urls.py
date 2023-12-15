from django.urls import path, include
from backendCV import views

urlpatterns = [
    #------ LOGIN AND REGISTER URLs ------#
    path('login', views.UserLoginView.as_view(), name='login'),
    path('register', views.UserRegistrationView.as_view(), name='register'),
    path('change-password', views.ChangePasswordView.as_view(), name='change-password'),
    path('refresh-token', views.RefreshTokenView.as_view(), name='refresh-token'),

    #------ USER URLs ------#
    path('user', views.UserList.as_view(), name='user-list'),
    path('user/<int:id>', views.UserForId.as_view(), name='user-detail'),
    
    #------ DEPARTMENT URLs ------#
    path('department', views.DepartmentList.as_view(), name='department-list'),
    
    #------ CORE URLs ------#
    path('core', views.CoreList.as_view(), name='core-list'),
    
    #------ POSITION URLs ------#
    path('position', views.PositionList.as_view(), name='position-list'),
    
    # ------ AREAS URLs ------#
    path('areas', views.AreasListCreateView.as_view(), name='area-list'),
    path('areas/create', views.AreasListCreateView.as_view(), name='area-create'),
    path('areas/<int:pk>', views.AreasDetailUpdateDestroyView.as_view(), name='area-detail'),
    path('areas/update/<int:pk>', views.AreasDetailUpdateDestroyView.as_view(), name='area-update'),
    path('areas/delete/<int:pk>', views.AreasDetailUpdateDestroyView.as_view(), name='area-delete'),
    
    # ------ Company URLs ------#
    path('companies', views.CompanyListCreateView.as_view(), name='company-list'),
    path('companies/create', views.CompanyListCreateView.as_view(), name='company-create'),
    path('companies/<int:pk>', views.CompanyDetailUpdateDestroyView.as_view(), name='company-detail'),
    path('companies/update/<int:pk>', views.CompanyDetailUpdateDestroyView.as_view(), name='company-update'),
    path('companies/delete/<int:pk>', views.CompanyDetailUpdateDestroyView.as_view(), name='company-delete'),
    
    # ------ PROFORMA URLs ------#
    path('proformas', views.ProformaListCreateView.as_view(), name='proforma-list'),
    path('proformas/create', views.ProformaListCreateView.as_view(), name='proforma-create'),
    path('proformas/<int:pk>', views.ProformaDetailUpdateDestroyView.as_view(), name='proforma-detail'),
    path('proformas/update/<int:pk>', views.ProformaDetailUpdateDestroyView.as_view(), name='proforma-update'),
    path('proformas/delete/<int:pk>', views.ProformaDetailUpdateDestroyView.as_view(), name='proforma-delete'),
    
    # ------ Employees URLs ------#
    path('employees', views.EmployeesListCreateView.as_view(), name='employee-list'),
    path('employees/create', views.EmployeesListCreateView.as_view(), name='employee-create'),
    path('employees/<int:pk>', views.EmployeesDetailUpdateDestroyView.as_view(), name='employee-detail'),
    path('employees/update/<int:pk>', views.EmployeesDetailUpdateDestroyView.as_view(), name='employee-update'),
    path('employees/delete/<int:pk>', views.EmployeesDetailUpdateDestroyView.as_view(), name='employee-delete'),

    # ------ INVOICE URLs ------#
    path('invoices', views.InvoiceListCreateView.as_view(), name='invoice-list'),
    path('invoices/create', views.InvoiceListCreateView.as_view(), name='invoice-create'),
    path('invoices/update/<int:pk>', views.InvoiceUpdateDestroyView.as_view(), name='invoice-update'),
    path('invoices/delete/<int:pk>', views.InvoiceUpdateDestroyView.as_view(), name='invoice-delete'),
    path('invoices/<int:client_id>/client', views.InvoiceSearchByClientView.as_view(), name='invoice-search-by-client'),

     # ------ CLIENT URLs ------#
    path('clients', views.ClientListCreateView.as_view(), name='client-list'),
    path('clients/create', views.ClientListCreateView.as_view(), name='client-create'),
    path('clients/update/<int:pk>', views.ClientUpdateDestroyView.as_view(), name='client-update'),
    path('clients/delete/<int:pk>', views.ClientUpdateDestroyView.as_view(), name='client-delete'),

    # ------ EXPENSE URLs ------#
    path('expenses', views.ExpenseListCreateView.as_view(), name='expense-list'),
    path('expenses/create', views.ExpenseListCreateView.as_view(), name='expense-create'),
    path('expenses/<int:pk>', views.ExpenseDetailUpdateDestroyView.as_view(), name='expense-detail'),
    path('expenses/update/<int:pk>', views.ExpenseDetailUpdateDestroyView.as_view(), name='expense-update'),
    path('expenses/delete/<int:pk>', views.ExpenseDetailUpdateDestroyView.as_view(), name='expense-delete'),
    path('expenses/<int:pk>/update-status/<int:new_status_id>', views.ExpenseDetailUpdateDestroyView.as_view(), name='expense-update-status'),
]