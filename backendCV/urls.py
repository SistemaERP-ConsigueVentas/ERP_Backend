from django.urls import path, include
from backendCV import views

urlpatterns = [
    #------ LOGIN AND REGISTER URLs ------#
    path('login', views.UserLoginView.as_view(), name='login'),
    path('register', views.UserRegistrationView.as_view(), name='register'),
    
    #------ EMPLOYEE URLs ------#
    path('employee/list', views.EmployeeList.as_view(), name='employee-list'),
    
    #------ COMPANY URL ------#
    path('company/list', views.CompanyList.as_view(), name='company-list'),
        
]