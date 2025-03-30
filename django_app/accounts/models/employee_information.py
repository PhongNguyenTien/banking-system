from django.db import models
from .employee_account import EmployeeAccount


class EmployeeInformation(models.Model):
    employee = models.OneToOneField(
        EmployeeAccount, 
        on_delete=models.CASCADE,
        related_name='information'
    )
    full_name = models.CharField(max_length=255)
    age = models.PositiveIntegerField()
    address = models.TextField()
    phone_number = models.CharField(max_length=20)
    employee_code = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'employee_information' 