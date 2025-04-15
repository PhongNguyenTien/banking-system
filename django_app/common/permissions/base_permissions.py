from rest_framework.permissions import BasePermission
from accounts.models.customer_account import CustomerAccount
from accounts.models.employee_account import EmployeeAccount
from accounts.models.role import ROLES
from rest_framework.exceptions import PermissionDenied

class RBACPermission(BasePermission):
    """
    Base class for role-based access control using DRF's BasePermission.
    Subclasses should define:
    - resource: the resource name in PERMISSIONS
    - PERMISSIONS: the permission structure
    """
    resource = None
    PERMISSIONS = {}
    
    def has_permission(self, request, view):
        """
        Check if the user has permission to perform the action.
        Maps to DRF's has_permission method.
        """
        user = request.user
        action = getattr(view, 'action', None)
        
        # If action is not set (for APIView), derive it from HTTP method
        if action is None:
            action = self._get_action_from_method(request.method)
            
        if not user.is_authenticated:
            return False
            
        # Get permission settings for this action
        permission_settings = self.get_permission_settings(action)
        if not permission_settings:
            return False
            
        # Check if user has required role
        allowed_roles = permission_settings.get('roles', [])
        
        # If user is a CustomerAccount, check if CUSTOMER role is allowed
        if isinstance(user, CustomerAccount):
            if ROLES.get('CUSTOMER') in allowed_roles:
                return True
            return False
        
        # If user is an EmployeeAccount, check roles
        if isinstance(user, EmployeeAccount):
            user_roles = [employee_role.role.id for employee_role in user.roles.all()]
            if set(user_roles) & set(allowed_roles):  # Intersection of sets
                return True
            return False
            
        return False
    
    def has_object_permission(self, request, view, obj):
        """
        Check if the user has permission to access the object.
        Maps to DRF's has_object_permission method.
        """

        action = getattr(view, 'action', None)
        
        # If action is not set (for APIView), derive it from HTTP method
        if action is None:
            action = self._get_action_from_method(request.method)
        
        # Get permission settings for this action
        permission_settings = self.get_permission_settings(action)
        if not permission_settings:
            return False
            
        # If no object permissions specified, rely on has_permission
        if 'object_permission' not in permission_settings:
            return True
            
        permission_type = permission_settings['object_permission']
        return self.check_object_permission(request, action, obj, permission_type)
    
    def get_permission_settings(self, action):
        """Get permission settings for a specific action."""
        return self.PERMISSIONS.get(self.resource, {}).get(action, {})
    
    def check_object_permission(self, request, action, obj, permission_type):
        """Check object-level permissions."""
        # Handle multiple permissions (all must pass)
        if isinstance(permission_type, list):
            errors = []
            for permission in permission_type:
                try:
                    result = self._check_single_permission(request, action, obj, permission)
                    if not result:
                        errors.append(f"Permission check '{permission}' failed.")
                except PermissionDenied as e:
                    errors.append(str(e))
                    
            if errors:
                raise PermissionDenied("; ".join(errors))
            
            return True
        
        # Handle single permission
        return self._check_single_permission(request, action, obj, permission_type)
    
    def _check_single_permission(self, request, action, obj, permission_type):
        """Check a single object-level permission."""
        if hasattr(self, permission_type):
            permission_method = getattr(self, permission_type)
            return permission_method(request, obj)
        
        return False
    
    def _get_action_from_method(self, method):
        """Convert HTTP method to action name."""
        method_map = {
            'GET': 'retrieve' if 'pk' in request.parser_context.get('kwargs', {}) else 'list',
            'POST': 'create',
            'PUT': 'update',
            'PATCH': 'partial_update',
            'DELETE': 'destroy'
        }
        return method_map.get(method, 'retrieve')
