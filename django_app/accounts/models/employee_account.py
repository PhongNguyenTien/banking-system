from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db.models import Max
import re


class EmployeeAccountManager(BaseUserManager):
    def _generate_employee_code(self, role):
        role_prefix_map = {
            EmployeeAccount.TRANSACTION_OFFICER: 'TO',
            EmployeeAccount.CREDIT_MANAGER: 'CM',
            EmployeeAccount.CREDIT_ANALYST: 'CA',
            EmployeeAccount.ADMIN: 'AD',
            EmployeeAccount.AUDIT: 'AU'
        }
        
        prefix = role_prefix_map.get(role)
        if not prefix:
            raise ValueError('Invalid role')

        # Find the last code with this prefix
        last_code = self.model.objects.filter(
            employee_code__startswith=prefix
        ).aggregate(Max('employee_code'))['employee_code__max']

        if not last_code:
            return f"{prefix}001"

        # Extract the number from the last code
        match = re.search(r'\d+$', last_code)
        if not match:
            return f"{prefix}001"

        last_number = int(match.group())
        new_number = last_number + 1
        return f"{prefix}{new_number:03d}"

    def create_user(self, username, password, role, **extra_fields):
        if not username:
            raise ValueError('Username is required')
        if not role:
            raise ValueError('Role is required')
        user = self.model(
            employee_code=self._generate_employee_code(role),
            role=role,
            username=username,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, password=None, **extra_fields):
        role = EmployeeAccount.ADMIN
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, password, role, **extra_fields)


class EmployeeAccount(AbstractBaseUser, PermissionsMixin):
    ADMIN = 1
    CREDIT_ANALYST = 2
    CREDIT_MANAGER = 3
    TRANSACTION_OFFICER = 4
    AUDIT = 5
    ROLE_CHOICES = [
        (1, 'Admin'),
        (2, 'Credit Analysis'),
        (3, 'Credit Manager'),
        (4, 'Transaction Officer'),
        (5, 'Audit'),
    ]

    employee_code = models.CharField(max_length=50, unique=True)
    username = models.CharField(max_length=150, unique=True)
    role = models.IntegerField(choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = EmployeeAccountManager()

    USERNAME_FIELD = 'username'

    class Meta:
        db_table = 'employee_accounts'
        
ROLES = {
    "ADMIN": EmployeeAccount.ADMIN,
    "CREDIT_ANALYST": EmployeeAccount.CREDIT_ANALYST,
    "CREDIT_MANAGER": EmployeeAccount.CREDIT_MANAGER,
    "TRANSACTION_OFFICER": EmployeeAccount.TRANSACTION_OFFICER,
    "AUDIT": EmployeeAccount.AUDIT,
}
