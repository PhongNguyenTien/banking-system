from accounts.models.role import ROLES
from rest_framework.exceptions import PermissionDenied
from accounts.models.employee_account import EmployeeAccount
from accounts.models.customer_account import CustomerAccount
from common.permissions.base_permissions import RBACPermission


class EmployeeAccountPermission(RBACPermission):
    PERMISSIONS = {
        'employee_account': {
            'create': {
                'roles': [ROLES['ADMIN']],
            },
            'list': {
                'roles': [ROLES['ADMIN']],
            },
            'retrieve': {
                'roles': [ROLES['ADMIN'], ROLES['TRANSACTION_OFFICER'], ROLES['CREDIT_ANALYST'], ROLES['CREDIT_MANAGER'], ROLES['AUDITOR']],
                'object_permission': 'is_owner',
            },
            'partial_update': {
                'roles': [ROLES['ADMIN'], ROLES['TRANSACTION_OFFICER'], ROLES['CREDIT_ANALYST'], ROLES['CREDIT_MANAGER'], ROLES['AUDITOR']],
                'object_permission': ['is_owner', 'can_update_only_username_and_password'],
            },
            'destroy': {
                'roles': [ROLES['ADMIN']]
            },
        },
    }
    resource = 'employee_account'

    # def __init__(self, action):
    #     self.action = action
        
    def is_owner(self, request, obj):
        print("request.user", request.user.id)
        print("obj", obj.id)
        if isinstance(request.user, EmployeeAccount) and request.user.id == obj.id:
            return True
        raise PermissionDenied("You can only access your own account")
    
    def can_update_only_username_and_password(self, request, obj):
        if request.method == 'PUT' or request.method == 'PATCH':
            return request.data and set(request.data.keys()).issubset({'username', 'password'})
        raise PermissionDenied("You can only update the username and password")
        
    # def check_object_permission(self, request, action, obj, permission_type):
    #     has_permission = super().check_object_permission(request, action, obj, permission_type)
    #     return has_permission


class CustomerAccountPermission(RBACPermission):
    PERMISSIONS = {
        'customer_account': {
            'create': {
                'roles': [ROLES['CUSTOMER']],
            },
            'list': {
                'roles': [ROLES['ADMIN']],
            },
            'retrieve': {
                'roles': [ROLES['CUSTOMER']],
                'object_permission': 'is_owner',
            },
            'partial_update': {
                'roles': [ROLES['CUSTOMER']],
                'object_permission': ['is_owner', 'can_update_only_email_and_password'],
            },
            'destroy': {
                'roles': [ROLES['ADMIN']],
            },
        },
    }
    resource = 'customer_account'

    # def __init__(self, action):
    #     self.action = action

    def is_owner(self, request, obj):
        """Check if user is the owner of this account."""
        if isinstance(request.user, CustomerAccount) and request.user.id == obj.id:
            return True
        raise PermissionDenied("You can only access your own account")
    
    def can_update_only_email_and_password(self, request, obj):
        if request.method == 'PUT' or request.method == 'PATCH':
            return request.data and set(request.data.keys()).issubset({'customer_email', 'password'})
        raise PermissionDenied("You can only update the email and password")
        
    # def check_object_permission(self, request, action, obj, permission_type):
    #     """Custom object permission checks."""
    #     # First check standard permissions
    #     has_permission = super().check_object_permission(request, action, obj, permission_type)
    #     return has_permission

class RolePermission(RBACPermission):
    PERMISSIONS = {
        'role': {
            'create': {
                'roles': [ROLES['ADMIN']],
            },
            'list': {
                'roles': [ROLES['ADMIN']],
            },
            'retrieve': {
                'roles': [ROLES['ADMIN']],
            },
            'update': {
                'roles': [ROLES['ADMIN']],
            },
            'partial_update': {
                'roles': [ROLES['ADMIN']],
            },
            'destroy': {
                'roles': [ROLES['ADMIN']],
            },
        },
    }
    resource = 'role'

    # def __init__(self, action):
    #     self.action = action

class RoleAssignmentPermission(RBACPermission):
    PERMISSIONS = {
        'role_assignment': {
            'assign': {
                'roles': [ROLES['ADMIN']],
            },
        },
    }
    resource = 'role_assignment'

    # def __init__(self, action):
    #     self.action = action
