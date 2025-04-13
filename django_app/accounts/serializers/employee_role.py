from rest_framework import serializers
from ..models.employee_role import EmployeeRole
from ..models.employee_account import EmployeeAccount
from ..models.role import Role

class EmployeeRoleAssignSerializer(serializers.Serializer):
    employee_id = serializers.IntegerField(required=True)
    role_id = serializers.IntegerField(required=True)
    
    def validate(self, data):
        # Validate employee exists
        try:
            employee = EmployeeAccount.objects.get(pk=data['employee_id'])
        except EmployeeAccount.DoesNotExist:
            raise serializers.ValidationError({"employee_id": "Employee does not exist"})
            
        # Validate role exists
        try:
            role = Role.objects.get(pk=data['role_id'])
        except Role.DoesNotExist:
            raise serializers.ValidationError({"role_id": "Role does not exist"})
            
        # Check if this role is already assigned to the employee
        if EmployeeRole.objects.filter(employee=employee, role=role).exists():
            raise serializers.ValidationError({"non_field_errors": "This role is already assigned to this employee"})
            
        # Store objects for create method
        data['employee'] = employee
        data['role'] = role
        
        return data
    
    def create(self, validated_data):
        return EmployeeRole.objects.create(
            employee=validated_data['employee'],
            role=validated_data['role']
        )
