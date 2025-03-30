import re
from django.db.models import Max
from ..models.role import Role


def generate_employee_code(role_id, model_class):
    role_prefix_map = {
        Role.TRANSACTION_OFFICER: 'TO',
        Role.CREDIT_MANAGER: 'CM',
        Role.CREDIT_ANALYST: 'CA',
        Role.ADMIN: 'AD',
        Role.AUDITOR: 'AU'
    }
    
    prefix = role_prefix_map.get(role_id)
    if not prefix:
        raise ValueError('Invalid role')

    # Find the last code with this prefix
    last_code = model_class.objects.filter(
        employee_code__startswith=prefix
    ).aggregate(Max('employee_code'))['employee_code__max']

    if not last_code:
        return f"{prefix}001"

    # Extract the number from the last code
    match = re.search(r'\d+$', last_code)
    if not match:
        return f"{prefix}001"

    last_number = int(match.group())
    new_number = last_number + 1
    return f"{prefix}{new_number:03d}" 