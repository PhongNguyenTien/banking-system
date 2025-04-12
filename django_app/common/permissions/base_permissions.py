from functools import wraps
from rest_framework.exceptions import PermissionDenied

from accounts.models.role import ROLES
from accounts.models.customer_account import CustomerAccount
class BasePermission:
    """Base class for permission checking."""
    PERMISSIONS = NotImplemented
    resource = NotImplemented

    def check_permission(self, request, action, obj=None):
        user = request.user

        if not user.is_authenticated:
            raise PermissionDenied("Authentication required.")
        
        allowed_roles = self.get_allowed_roles(action)
        
        if isinstance(user, CustomerAccount):
            if obj:
                return self.check_object_permission(request, action, obj)
            if ROLES['CUSTOMER'] in allowed_roles:
                return True
            return False


        # Get user roles properly - user.roles is a related manager, not a direct attribute
        user_roles = [employee_role.role.id for employee_role in user.roles.all()]

        if set(user_roles).issubset(allowed_roles):
            return True

        # Object-level checks (if an object is provided)
        if obj:
            return self.check_object_permission(request, action, obj)

        return False

    def get_allowed_roles(self, action):
        return self.PERMISSIONS.get(self.resource, {}).get(action, [])
    
    def check_object_permission(self, request, action, obj):
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
