from django.db import models
from .employee_account import EmployeeAccount
from .role import Role


class EmployeeRole(models.Model):
    employee = models.ForeignKey(
        EmployeeAccount,
        on_delete=models.CASCADE,
        related_name='roles'
    )
    role = models.ForeignKey(
        Role,
        on_delete=models.PROTECT
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'employee_roles'
        unique_together = ('employee', 'role') 