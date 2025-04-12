from django.contrib.auth.backends import ModelBackend
from .models.employee_account import EmployeeAccount
from .models.customer_account import CustomerAccount

class MultiModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # Try to authenticate as an employee first
        employee = None
        try:
            employee = EmployeeAccount.objects.get(username=username)
            if employee.check_password(password):
                return employee
        except EmployeeAccount.DoesNotExist:
            pass
            
        # If employee authentication fails, try customer authentication
        try:
            customer = CustomerAccount.objects.get(customer_email=username)
            if customer.check_password(password):
                return customer
        except CustomerAccount.DoesNotExist:
            pass
            
        return None
        
    def get_user(self, user_id):
        try:
            return EmployeeAccount.objects.get(pk=user_id)
        except EmployeeAccount.DoesNotExist:
            try:
                return CustomerAccount.objects.get(pk=user_id)
            except CustomerAccount.DoesNotExist:
                return None 