from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.settings import api_settings
from .models.employee_account import EmployeeAccount
from .models.customer_account import CustomerAccount

class CustomJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        """
        Attempts to find and return a user using the given validated token.
        """
        try:
            user_id = validated_token[api_settings.USER_ID_CLAIM]
            user_type = validated_token.get('user_type', 'employee')  # Default to employee if not specified
            
            if user_type == 'customer':
                return CustomerAccount.objects.get(pk=user_id)
            else:
                return EmployeeAccount.objects.get(pk=user_id)
                
        except (EmployeeAccount.DoesNotExist, CustomerAccount.DoesNotExist):
            return None 