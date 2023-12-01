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