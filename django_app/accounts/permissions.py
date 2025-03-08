from rest_framework import permissions
from accounts.models import EmployeeAccount, CustomerAccount

class EmployeeAccountPermission(permissions.BasePermission):
    """
    Permission class for employee accounts:
    - Admins can perform all operations
    - Other employees can only update username and password of their own account
    """
    def has_permission(self, request, view):
        """
        General permission checks for the entire view/endpoint.
        Controls access to:
        - LIST: /api/accounts/employees/
        - CREATE: POST to /api/accounts/employees/
        """
        # Only Admin can create, list, or access other actions
        if view.action in ['create', 'list']:
            return request.user.role == EmployeeAccount.ADMIN
            
        # For other actions (retrieve, update, delete), let has_object_permission decide
        if view.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return True
            
        # Deny any other actions
        return False
        
    def has_object_permission(self, request, view, obj):
        """
        Object-level permission checks.
        Controls access to:
        - RETRIEVE: /api/accounts/employees/{id}/
        - UPDATE: PUT/PATCH to /api/accounts/employees/{id}/
        - DELETE: DELETE to /api/accounts/employees/{id}/
        """
        # Admin has full access to any employee account
        if request.user.role == EmployeeAccount.ADMIN:
            return True
            
        # Employees can view and update only username and password of their own account
        if isinstance(request.user, EmployeeAccount) and request.user.id == obj.id:
            if view.action == 'retrieve':
                return True
                
            if view.action in ['update', 'partial_update']:
                # Check if only allowed fields are being updated
                allowed_fields = {'username', 'password'}
                if request.data and set(request.data.keys()).issubset(allowed_fields):
                    return True
                return False
                
            # Users cannot delete their own account
            if view.action == 'destroy':
                return False
                
        # Deny access for all other cases
        return False

class CustomerAccountPermission(permissions.BasePermission):
    """
    Permission class for customer accounts:
    - Transaction officers can create and view customer accounts
    - Customers can view and update only email and password of their own account
    """
    def has_permission(self, request, view):
        """
        General permission checks for the entire view/endpoint.
        """
        if view.action == 'create':
            return request.user.role == EmployeeAccount.ADMIN

        # Only Transaction Officer can create
        if view.action == 'list':
            return request.user.role in [EmployeeAccount.TRANSACTION_OFFICER, EmployeeAccount.ADMIN]

        # For other actions (retrieve, update, delete), let has_object_permission decide
        if view.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return True
            
        # Deny any other actions
        return False
        
    def has_object_permission(self, request, view, obj):
        """
        Object-level permission checks.
        """
        # Transaction Officer has full access to any customer account
        if request.user.role in [EmployeeAccount.TRANSACTION_OFFICER, EmployeeAccount.ADMIN]:
            return True
            
        # Customers can view and update only email and password of their own account
        if isinstance(request.user, CustomerAccount) and request.user.id == obj.id:
            if view.action == 'retrieve':
                return True
                
            if view.action in ['update', 'partial_update']:
                # Check if only allowed fields are being updated
                allowed_fields = {'customer_email', 'password'}
                if request.data and set(request.data.keys()).issubset(allowed_fields):
                    return True
                return False
                
            # Customers cannot delete their account
            if view.action == 'destroy':
                return False
                
        # Deny access for all other cases
        return False
    