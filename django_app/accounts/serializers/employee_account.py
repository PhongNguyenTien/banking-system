from rest_framework import serializers
from ..models.employee_account import EmployeeAccount
from ..models.employee_information import EmployeeInformation
from ..models.employee_role import EmployeeRole
from ..models.role import Role
from ..utils.employee_code_generator import generate_employee_code

class EmployeeAccountSerializer(serializers.ModelSerializer):
    employee_code = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()
    roles = serializers.SerializerMethodField()
    
    class Meta:
        model = EmployeeAccount
        fields = ['id', 'username', 'is_active', 'created_at', 'employee_code', 'full_name', 'roles']
        read_only_fields = ['created_at', 'employee_code', 'roles']
    
    def get_employee_code(self, obj):
        if hasattr(obj, 'information'):
            return obj.information.employee_code
        return None
    
    def get_full_name(self, obj):
        if hasattr(obj, 'information'):
            return obj.information.full_name
        return None
    
    def get_roles(self, obj):
        return [{'id': role.role.id, 'name': role.role.name} 
                for role in obj.roles.select_related('role').all()]

class EmployeeAccountCreateSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(required=True, write_only=True)
    age = serializers.IntegerField(required=True, write_only=True)
    address = serializers.CharField(required=True, write_only=True)
    phone_number = serializers.CharField(required=True, write_only=True)
    role_id = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all(), write_only=True)
    
    class Meta:
        model = EmployeeAccount
        fields = ['username', 'password', 'full_name', 'age', 'address', 'phone_number', 'role_id']
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        role_id = validated_data.pop('role_id')
        full_name = validated_data.pop('full_name')
        age = validated_data.pop('age')
        address = validated_data.pop('address')
        phone_number = validated_data.pop('phone_number')
        
        # Create the employee account
        employee = EmployeeAccount.objects.create_user(**validated_data)
        
        # Create employee information with generated code
        employee_code = generate_employee_code(role_id.id, EmployeeInformation)
        EmployeeInformation.objects.create(
            employee=employee,
            full_name=full_name,
            age=age,
            address=address,
            phone_number=phone_number,
            employee_code=employee_code
        )
        
        # Assign role
        EmployeeRole.objects.create(
            employee=employee,
            role=role_id
        )
        
        return employee