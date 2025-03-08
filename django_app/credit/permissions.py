from rest_framework import permissions
from accounts.models import EmployeeAccount, CustomerAccount


class CreditPackagePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ['create', 'update', 'partial_update', 'destroy']:
            return request.user.role == EmployeeAccount.ADMIN
        return True

class CustomerProfilePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        """
        General permission checks for the entire view/endpoint.
        Controls access to:
        - LIST: /api/credit/customers/
        - CREATE: POST to /api/credit/customers/
        """

        # Only Transaction Officer can create
        if view.action == 'create':
            return request.user.role == EmployeeAccount.TRANSACTION_OFFICER

        # For listing profiles
        if view.action == 'list':
            # Only Transaction Officer can see all profiles
            # Customers can access list (but will be filtered in queryset)
            return (request.user.role == EmployeeAccount.TRANSACTION_OFFICER or 
                   isinstance(request.user, CustomerAccount))

        # For other actions (retrieve, update, delete), let has_object_permission decide
        if view.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return True

        # Deny any other actions
        return False

    def has_object_permission(self, request, view, obj):
        """
        Object-level permission checks.
        Controls access to:
        - RETRIEVE: /api/credit/customers/{id}/
        - UPDATE: PUT/PATCH to /api/credit/customers/{id}/
        - DELETE: DELETE to /api/credit/customers/{id}/
        """
        # Transaction Officer has full access to any object
        if request.user.role == EmployeeAccount.TRANSACTION_OFFICER:
            return True
        
        # Credit Analysts can only view profiles
        if request.user.role == EmployeeAccount.CREDIT_ANALYST:
            return view.action == 'retrieve'

        # Customers can only view and update their own profile
        if isinstance(request.user, CustomerAccount):
            is_own_profile = obj.id == request.user.customer_profile.id
            # Allow read and update for own profile
            if view.action in ['retrieve', 'update', 'partial_update']:
                return is_own_profile
            # Deny delete even for own profile
            if view.action == 'destroy':
                return False

        # Deny access for all other roles
        return False
    
class CreditApplicationPermission(permissions.BasePermission):
    """
    Permission class for credit applications:
    - Transaction officers can perform all operations
    - Credit analysts can only view applications
    - Auditors can only view (list and retrieve) applications
    """
    def has_permission(self, request, view):
        """
        General permission checks for the entire view/endpoint.
        Controls access to:
        - LIST: /api/credit/applications/
        - CREATE: POST to /api/credit/applications/
        """
        # Only Transaction Officer can create
        if view.action == 'create':
            return request.user.role == EmployeeAccount.TRANSACTION_OFFICER

        # For listing applications
        if view.action == 'list':
            # Transaction Officer, Credit Analyst, Credit Manager, and Auditor can see all applications
            return request.user.role in [
                EmployeeAccount.TRANSACTION_OFFICER,
                EmployeeAccount.CREDIT_ANALYST,
                EmployeeAccount.CREDIT_MANAGER,
                EmployeeAccount.AUDIT,
            ]

        # For other actions (retrieve, update, delete), let has_object_permission decide
        if view.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return True

        # Deny any other actions
        return False

    def has_object_permission(self, request, view, obj):
        """
        Object-level permission checks.
        Controls access to:
        - RETRIEVE: /api/credit/applications/{id}/
        - UPDATE: PUT/PATCH to /api/credit/applications/{id}/
        - DELETE: DELETE to /api/credit/applications/{id}/
        """
        # Transaction Officer has full access to any application
        if request.user.role == EmployeeAccount.TRANSACTION_OFFICER:
            return True

        # Credit Analyst and Credit Manager can only view applications
        if request.user.role in [EmployeeAccount.CREDIT_ANALYST, EmployeeAccount.CREDIT_MANAGER]:
            return view.action == 'retrieve'
            
        # Auditor can only view applications
        if request.user.role == EmployeeAccount.AUDIT:
            return view.action == 'retrieve'

        # Deny access for all other roles
        return False


class CreditAssessmentPermission(permissions.BasePermission):
    """
    Permission class for credit assessments:
    - Credit analysts can perform all operations
    - Credit managers can only view and update status
    - Auditors can only view (list and retrieve) assessments
    """
    def has_permission(self, request, view):
        """
        General permission checks for the entire view/endpoint.
        Controls access to:
        - LIST: /api/credit/assessments/
        - CREATE: POST to /api/credit/assessments/
        """
        # Only Credit Analyst can create
        if view.action == 'create':
            return request.user.role == EmployeeAccount.CREDIT_ANALYST

        # For listing assessments
        if view.action == 'list':
            # Credit Analyst, Credit Manager, and Auditor can see assessments
            return request.user.role in [
                EmployeeAccount.CREDIT_ANALYST,
                EmployeeAccount.CREDIT_MANAGER,
                EmployeeAccount.AUDIT,
            ]

        # For other actions (retrieve, update, delete), let has_object_permission decide
        if view.action in ['retrieve', 'update', 'partial_update', 'destroy', 'update_status']:
            return True

        # Deny any other actions
        return False

    def has_object_permission(self, request, view, obj):
        """
        Object-level permission checks.
        Controls access to:
        - RETRIEVE: /api/credit/assessments/{id}/
        - UPDATE: PUT/PATCH to /api/credit/assessments/{id}/
        - DELETE: DELETE to /api/credit/assessments/{id}/
        """
        # Credit Analyst has full access to any assessment
        if request.user.role == EmployeeAccount.CREDIT_ANALYST:
            return True

        # Credit Manager can only view and update status
        if request.user.role == EmployeeAccount.CREDIT_MANAGER:
            return view.action in ['retrieve', 'update_status']
            
        # Auditor can only view assessments
        if request.user.role == EmployeeAccount.AUDIT:
            return view.action == 'retrieve'

        # Deny access for all other roles
        return False
