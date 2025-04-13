from functools import wraps
from rest_framework.exceptions import PermissionDenied
from accounts.models.customer_account import CustomerAccount
from accounts.models.employee_account import EmployeeAccount
from accounts.models.role import ROLES

class BasePermission:
    """Base class for permission checking."""
    PERMISSIONS = NotImplemented
    resource = NotImplemented

    def check_permission(self, request, action, obj=None):
        user = request.user

        if not user.is_authenticated:
            raise PermissionDenied("Authentication required.")

        # Get permission settings for this action
        permission_settings = self.get_permission_settings(action)
        if not permission_settings:
            return False

        # Check if user has required role
        allowed_roles = permission_settings.get('roles', [])
        
        # If user is a CustomerAccount, check if CUSTOMER role is allowed
        if isinstance(user, CustomerAccount):
            if ROLES.get('CUSTOMER') in allowed_roles:
                # If there's an object and an object permission specified, check it
                if obj and 'object_permission' in permission_settings:
                    return self.check_object_permission(request, action, obj, permission_settings['object_permission'])
                return True
            # If no role access, may still have object-level permission
            elif obj and 'object_permission' in permission_settings:
                return self.check_object_permission(request, action, obj, permission_settings['object_permission'])
            return False
        
        # If user is an EmployeeAccount, check roles
        if isinstance(user, EmployeeAccount):
            user_roles = [employee_role.role.id for employee_role in user.roles.all()]
            print(user_roles)
            print(allowed_roles)
            print(permission_settings)
            print(request.method)
            if set(user_roles) & set(allowed_roles):  # Intersection of sets
                # If no role access, may still have object-level permission
                if obj and 'object_permission' in permission_settings:
                    return self.check_object_permission(request, action, obj, permission_settings['object_permission'])
                return True
            return False
        return False

    def get_permission_settings(self, action):
        """Get permission settings for a specific action."""
        return self.PERMISSIONS.get(self.resource, {}).get(action, {})
    
    def check_object_permission(self, request, action, obj, permission_type):
        """
        Check object-level permissions.
        Supports single permissions or lists of permissions.
        """
        # Handle multiple permissions (all must pass)
        if isinstance(permission_type, list):
            errors = []
            for permission in permission_type:
                try:
                    # Try the permission check
                    result = self._check_single_permission(request, action, obj, permission)
                    if not result:
                        errors.append(f"Permission check '{permission}' failed.")
                except PermissionDenied as e:
                    # Collect the specific error message
                    errors.append(str(e))
                    
            # If any errors were collected, raise PermissionDenied with all messages
            if errors:
                raise PermissionDenied("; ".join(errors))
            
            # All permissions passed
            return True
        
        # Handle single permission
        return self._check_single_permission(request, action, obj, permission_type)
        

    def _check_single_permission(self, request, action, obj, permission_type):
        """Check a single object-level permission."""
        # Special permission handler - call methods directly if they exist
        if hasattr(self, permission_type):
            # Call the method with the same name as permission_type
            permission_method = getattr(self, permission_type)
            return permission_method(request, obj)
        
        return False

def has_permission(permission_checker):
    """Decorator that uses a PermissionChecker instance."""
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(instance, request, *args, **kwargs):
            obj = None
            if 'pk' in kwargs:
                obj = instance.get_object()  # Get object *before* permission check

            if permission_checker.check_permission(request, permission_checker.action, obj):
                return view_func(instance, request, *args, **kwargs)
            else:
                raise PermissionDenied("You do not have permission.")
        return _wrapped_view
    return decorator
