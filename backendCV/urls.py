from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

from backendCV import views

urlpatterns = [
    #------ LOGIN URL ------#
    path('login', obtain_auth_token, name='login'),
    
    #------ EMPLOYEE URLs ------#
    path('employee/list', views.EmployeeList.as_view(), name='employee-list'),
    
    #------ COMPANY URL ------#
    path('company/list', views.CompanyList.as_view(), name='company-list'),
    
]