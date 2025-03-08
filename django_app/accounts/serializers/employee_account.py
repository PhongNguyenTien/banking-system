from rest_framework import serializers
from accounts.models import EmployeeAccount

class EmployeeAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeAccount
        fields = ['id', 'employee_code', 'username', 'role', 'is_active', 'created_at']
        read_only_fields = ['created_at']

class EmployeeAccountCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = EmployeeAccount
        fields = ['username', 'password', 'role']

    def create(self, validated_data):
        return EmployeeAccount.objects.create_user(**validated_data)