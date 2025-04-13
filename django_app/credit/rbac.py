from accounts.models.role import ROLES  # Import ROLES
from common.permissions.base_permissions import BasePermission  # Import the base class
from rest_framework.exceptions import PermissionDenied
from accounts.models.employee_account import EmployeeAccount
from accounts.models.customer_account import CustomerAccount
class CustomerProfilePermission(BasePermission):
    PERMISSIONS = {
        'customer_profile': {
            'create': {
                'roles': [ROLES['TRANSACTION_OFFICER']],
            },
            'list': {
                'roles': [ROLES['TRANSACTION_OFFICER']],
            },
            'retrieve': {
                'roles': [ROLES['CUSTOMER']],
                'object_permission': 'is_owner',
            },
            'update': {
                'roles': [ROLES['CUSTOMER']],
                'object_permission': ['is_owner', 'can_update_only_email_and_password'],
            },
            'destroy': {
                'roles': [ROLES['TRANSACTION_OFFICER']]
            },
        },
    }
    resource = 'customer_profile'

    def __init__(self, action):
        self.action = action
        
    def is_owner(self, request, obj):
        if isinstance(request.user, CustomerAccount) and obj.id == request.user.customer_profile.id:
            return True
        raise PermissionDenied("You can only access your own customer profile")
    
    def can_update_only_email_and_password(self, request, obj):
        if request.method == 'PUT' or request.method == 'PATCH':
            return request.data and set(request.data.keys()).issubset({'customer_email', 'password'})
        raise PermissionDenied("You can only update the email and password")

        
    def check_object_permission(self, request, action, obj, permission_type):
        has_permission = super().check_object_permission(request, action, obj, permission_type)
        return has_permission


class CreditAssessmentPermission(BasePermission):
    PERMISSIONS = {
        'credit_assessment': {
            'create': {
                'roles': [ROLES['CREDIT_ANALYST']],
            },
            'list': {
                'roles': [ROLES['CREDIT_MANAGER'], ROLES['AUDITOR']],
            },
            'retrieve': {
                'roles': [ROLES['CREDIT_ANALYST'], ROLES['CREDIT_MANAGER'], ROLES['AUDITOR'], ROLES['CUSTOMER']],
                'object_permission': ['is_owner', 'is_creator', 'is_credit_manager', 'is_auditor'],
            },
            'update': {
                'roles': [ROLES['CREDIT_ANALYST']],
                'object_permission': ['is_creator', 'can_update_only_risk_score_and_comments'],
            },
            'destroy': {
                'roles': [ROLES['CREDIT_ANALYST']],
                'object_permission': 'is_creator',
            },
            'update_status': {
                'roles': [ROLES['CREDIT_MANAGER']],
            },
        },
    }
    resource = 'credit_assessment'

    def __init__(self, action):
        self.action = action
        
    def is_creator(self, request, obj):
        if isinstance(request.user, EmployeeAccount) and request.user.roles.filter(role__id=ROLES['CREDIT_ANALYST']).exists() and request.user.id == obj.analyst.id:
            return True
        raise PermissionDenied("You can only access the credit assessment created by you")
    
    def is_owner(self, request, obj):
        if isinstance(request.user, CustomerAccount) and obj.application.customer_profile.id == request.user.customer_profile.id:
            return True
        raise PermissionDenied("You can only access the credit assessment of your application")
    
    def is_credit_manager(self, request, obj):
        if isinstance(request.user, EmployeeAccount) and request.user.roles.filter(role__id=ROLES['CREDIT_MANAGER']).exists():
            return True
        raise PermissionDenied("Only credit managers can perform this action")
    
    def is_auditor(self, request, obj):
        if isinstance(request.user, EmployeeAccount) and request.user.roles.filter(role__id=ROLES['AUDITOR']).exists():
            return True
        raise PermissionDenied("Only auditors can perform this action")
    
    def can_update_only_risk_score_and_comments(self, request, obj):
        if request.method == 'PUT' or request.method == 'PATCH':
            return request.data and set(request.data.keys()).issubset({'risk_score', 'comments'})
        raise PermissionDenied("You can only update the risk score and comments")
        
    def check_object_permission(self, request, action, obj, permission_type):
        has_permission = super().check_object_permission(request, action, obj, permission_type)
        return has_permission


class CreditApplicationPermission(BasePermission):
    PERMISSIONS = {
        'credit_application': {
            'create': {
                'roles': [ROLES['TRANSACTION_OFFICER']],
            },
            'list': {
                'roles': [ROLES['TRANSACTION_OFFICER'], ROLES['CREDIT_ANALYST'], ROLES['CREDIT_MANAGER'], ROLES['AUDITOR']],
            },
            'retrieve': {
                'roles': [ROLES['CUSTOMER']],
                'object_permission': 'is_owner',
            },
            'update': {
                'roles': [ROLES['TRANSACTION_OFFICER']],
            },
            'destroy': {
                'roles': [ROLES['TRANSACTION_OFFICER']],
            },
        },
    }
    resource = 'credit_application'
    
    def __init__(self, action):
        self.action = action
    
    def is_owner(self, request, obj):
        if isinstance(request.user, CustomerAccount) and obj.customer_profile.id == request.user.customer_profile.id:
            return True
        raise PermissionDenied("You can only access the credit application of your profile")
    
    def check_object_permission(self, request, action, obj, permission_type):
        has_permission = super().check_object_permission(request, action, obj, permission_type)
        return has_permission
    

class CreditPackagePermission(BasePermission):
    PERMISSIONS = {
        'credit_package': {
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
            'destroy': {
                'roles': [ROLES['ADMIN']],
            },
        },
    }
    resource = 'credit_package'

    def __init__(self, action):
        self.action = action
