from django.db import models


class Role(models.Model):
    ADMIN = 1
    CREDIT_ANALYST = 2
    CREDIT_MANAGER = 3
    TRANSACTION_OFFICER = 4
    AUDITOR = 5
    CUSTOMER = 6
    
    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (CREDIT_ANALYST, 'Credit Analyst'),
        (CREDIT_MANAGER, 'Credit Manager'),
        (TRANSACTION_OFFICER, 'Transaction Officer'),
        (AUDITOR, 'Audit'),
        (CUSTOMER, 'Customer'),
    ]
    
    name = models.CharField(max_length=50)
    
    class Meta:
        db_table = 'roles'
        
    def __str__(self):
        return self.name


# Create a dictionary for role lookup
ROLES = {
    "ADMIN": Role.ADMIN,
    "CREDIT_ANALYST": Role.CREDIT_ANALYST,
    "CREDIT_MANAGER": Role.CREDIT_MANAGER,
    "TRANSACTION_OFFICER": Role.TRANSACTION_OFFICER,
    "AUDITOR": Role.AUDITOR,
    "CUSTOMER": Role.CUSTOMER,
} 