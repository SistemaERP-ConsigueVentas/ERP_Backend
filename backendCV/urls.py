from django.urls import path, include

from backendCV import views

urlpatterns = [
    #------ USER URLs ------#
    path('user/list', views.UserList.as_view(), name='user-list'),
]