from django.urls import path, include
from backendCV import views

urlpatterns = [
    #------ LOGIN AND REGISTER URLs ------#
    path('login', views.UserLoginView.as_view(), name='login'),
    path('register', views.UserRegistrationView.as_view(), name='register'),
    path('change-password', views.ChangePasswordView.as_view(), name='change-password'),
    
    #------ USER URLs ------#
    path('user/list', views.UserList.as_view(), name='user-list'),
    path('user/<int:id>', views.UserForId.as_view(), name='user-detail'),
    
    #------ DEPARTMENT URLs ------#
    path('department/list', views.DepartmentList.as_view(), name='department-list'),
    
    #------ CORE URLs ------#
    path('core/list', views.CoreList.as_view(), name='core-list'),
    
    #------ POSITION URLs ------#
    path('position/list', views.PositionList.as_view(), name='position-list'),
    
    # #------ EMPLOYEE URLs ------#
    # path('profile/list', views.ProfileList.as_view(), name='profile-list'),
    
    # #------ EMPLOYEE URLs ------#
    # path('role/list', views.RoleList.as_view(), name='role-list'),
]