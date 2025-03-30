from rest_framework import serializers
from accounts.serializers.employee_account import EmployeeAccountSerializer
from ..models import AuditLog

class AuditLogSerializer(serializers.ModelSerializer):
    performed_by = EmployeeAccountSerializer(read_only=True)
    
    class Meta:
        model = AuditLog
        fields = [
            'id',
            'action',
            'entity_type',
            'entity_id',
            'details',
            'performed_by',
            'created_at'
        ] 