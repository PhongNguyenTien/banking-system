from accounts.models.employee_account import ROLES
from common.permissions.base_permissions import BasePermission
from rest_framework.exceptions import PermissionDenied
from accounts.models.employee_account import EmployeeAccount
from accounts.models.customer_account import CustomerAccount

class EmployeeAccountPermission(BasePermission):
    PERMISSIONS = {
        'employee_account': {
            'create': [ROLES['ADMIN']],
            'list': [ROLES['ADMIN']],
            'retrieve': [ROLES['ADMIN']],
            'update': [ROLES['ADMIN']],
            'destroy': [ROLES['ADMIN']],
        },
    }
    resource = 'employee_account'

    def __init__(self, action):
        self.action = action
        
    def check_object_permission(self, request, action, obj):
        user = request.user
        
        if isinstance(user, EmployeeAccount) and user.id == obj.id:
            if action == 'retrieve':
                return True
            if action == 'update':
                allowed_fields = {'username', 'password'}
                if request.data and set(request.data.keys()).issubset(allowed_fields):
                    return True
                raise PermissionDenied("You can only update username and password.")
            if action == 'destroy':
                raise PermissionDenied("Employees cannot delete their own accounts.")

        return False


class CustomerAccountPermission(BasePermission):
    PERMISSIONS = {
        'customer_account': {
            'create': [ROLES['ADMIN']],
            'list': [ROLES['ADMIN'], ROLES['TRANSACTION_OFFICER']],
            'retrieve': [ROLES['ADMIN'], ROLES['TRANSACTION_OFFICER']],
            'update': [ROLES['ADMIN'], ROLES['TRANSACTION_OFFICER']],
            'destroy': [ROLES['ADMIN']],
        },
    }
    resource = 'customer_account'

    def __init__(self, action):
        self.action = action

    def check_object_permission(self, request, action, obj):
        user = request.user
        
        if isinstance(user, CustomerAccount) and user.id == obj.id:
            if action == 'retrieve':
                return True
            if action == 'update':
                allowed_fields = {'customer_email', 'password'}
                if request.data and set(request.data.keys()).issubset(allowed_fields):
                    return True
                raise PermissionDenied("You can only update email and password")
            if action == 'destroy':
                raise PermissionDenied("Customers cannot delete their own accounts.")
            
        return False
