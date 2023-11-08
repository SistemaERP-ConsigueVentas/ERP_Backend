from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from backendCV import views
from backendCV.user.customToken import CustomAuthToken
from backendCV.user.register import register

urlpatterns = [
    #------ LOGIN URL ------#
    path('login', CustomAuthToken.as_view(), name='login'),
    path('register', register, name='register'),
    
    #------ EMPLOYEE URLs ------#
    path('employee/list', views.EmployeeList.as_view(), name='employee-list'),
    
    #------ COMPANY URL ------#
    path('company/list', views.CompanyList.as_view(), name='company-list'),
    
]