from rest_framework import serializers

from accounts.serializers.employee_account import EmployeeAccountSerializer
from ..models import CreditAssessment, CreditApplication
from accounts.models.employee_account import EmployeeAccount
from .credit_application import CreditApplicationSerializer


class CreditAssessmentSerializer(serializers.ModelSerializer):
    analyst = EmployeeAccountSerializer(read_only=True)
    application = CreditApplicationSerializer(read_only=True)

    class Meta:
        model = CreditAssessment
        fields = [
            'id',
            'application',
            'analyst',
            'risk_score',
            'comments',
            'status',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'analyst']

class CreditAssessmentCreateSerializer(serializers.ModelSerializer):
    application_id = serializers.PrimaryKeyRelatedField(
        queryset=CreditApplication.objects.all()
    )
    analyst = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = CreditAssessment
        fields = [
            'application_id',
            'risk_score',
            'comments',
            'analyst'
        ]
        
    def validate_application_id(self, value):
        # Check if application already has an assessment
        if hasattr(value, 'credit_assessment'):
            raise serializers.ValidationError("This application already has an assessment")
        return value
    
    def create(self, validated_data):
        request = self.context.get('request')
        analyst = request.user
        if not isinstance(analyst, EmployeeAccount) or analyst.role != EmployeeAccount.CREDIT_ANALYST:
            raise serializers.ValidationError("Only credit analysts can create assessments")
        application = validated_data.pop('application_id')
        credit_assessment = CreditAssessment.objects.create(
            application=application,
            analyst=analyst,
            status=CreditAssessment.UNDER_REVIEW,
            **validated_data
        )
        return credit_assessment
