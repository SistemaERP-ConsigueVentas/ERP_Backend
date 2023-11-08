from django.shortcuts import render
from rest_framework import generics, status
from backendCV.models import Employee, Company, User
from backendCV.serializers import EmployeeListSerializer, CompanyListSerializer
from rest_framework.permissions import IsAuthenticated

class EmployeeList(generics.ListAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeListSerializer
    permission_classes = [IsAuthenticated]
    

class CompanyList(generics.ListAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanyListSerializer
    permission_classes = [IsAuthenticated]
    
    
