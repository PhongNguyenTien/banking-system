from accounts.models.role import ROLES  # Import ROLES
from common.permissions.base_permissions import BasePermission  # Import the base class
from rest_framework.exceptions import PermissionDenied
from accounts.models.employee_account import EmployeeAccount

class CustomerProfilePermission(BasePermission):
    PERMISSIONS = {
        'customer_profile': {
            'create': [ROLES['TRANSACTION_OFFICER']],
            'list': [ROLES['TRANSACTION_OFFICER']],
            'retrieve': [ROLES['TRANSACTION_OFFICER'], ROLES['CREDIT_ANALYST']],
            'update': [ROLES['TRANSACTION_OFFICER']],
            'destroy': [ROLES['TRANSACTION_OFFICER']],
        },
    }
    resource = 'customer_profile'

    def __init__(self, action):
        self.action = action
        
    def check_object_permission(self, request, action, obj):
        user = request.user
        
        if hasattr(user, 'customer_profile') and obj.id == user.customer_profile.id:
            if action in ['retrieve', 'update']:
                return True
            if action == 'destroy':
                raise PermissionDenied("Customers cannot delete their own profile.")
                
        return False


class CreditAssessmentPermission(BasePermission):
    PERMISSIONS = {
        'credit_assessment': {
            'create': [ROLES['CREDIT_ANALYST']],
            'list': [ROLES['CREDIT_ANALYST'], ROLES['CREDIT_MANAGER'], ROLES['AUDITOR']],
            'retrieve': [ROLES['CREDIT_ANALYST'], ROLES['CREDIT_MANAGER'], ROLES['AUDITOR']],
            'update': [ROLES['CREDIT_ANALYST']],
            'destroy': [ROLES['CREDIT_ANALYST']],
            'update_status': [ROLES['CREDIT_MANAGER']],
        },
    }
    resource = 'credit_assessment'

    def __init__(self, action):
        self.action = action
        
    def check_object_permission(self, request, action, obj):
        user = request.user
        
        if isinstance(user, EmployeeAccount) and user.id == obj.analyst.id:
            if action in ['retrieve', 'update']:
                return True
            if action == 'destroy':
                raise PermissionDenied("Credit analysts cannot delete their own assessments.")
                
        return False


class CreditApplicationPermission(BasePermission):
    PERMISSIONS = {
        'credit_application': {
            'create': [ROLES['TRANSACTION_OFFICER']],
            'list': [ROLES['TRANSACTION_OFFICER'], ROLES['CREDIT_ANALYST'], ROLES['CREDIT_MANAGER'], ROLES['AUDITOR']],
            'retrieve': [ROLES['TRANSACTION_OFFICER'], ROLES['CREDIT_ANALYST'], ROLES['CREDIT_MANAGER'], ROLES['AUDITOR']],
            'update': [ROLES['TRANSACTION_OFFICER']],
            'destroy': [ROLES['TRANSACTION_OFFICER']],
        },
    }
    resource = 'credit_application'
    
    def __init__(self, action):
        self.action = action


class CreditPackagePermission(BasePermission):
    PERMISSIONS = {
        'credit_package': {
            'create': [ROLES['ADMIN']],
            'list': [ROLES['ADMIN']],
            'retrieve': [ROLES['ADMIN']],
            'update': [ROLES['ADMIN']],
            'destroy': [ROLES['ADMIN']],
        },
    }
    resource = 'credit_package'

    def __init__(self, action):
        self.action = action
