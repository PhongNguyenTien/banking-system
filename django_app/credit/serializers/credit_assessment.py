from rest_framework import serializers

from accounts.serializers.employee_account import EmployeeAccountSerializer
from ..models import CreditAssessment, CreditApplication

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

    class Meta:
        model = CreditAssessment
        fields = [
            'application_id',
            'risk_score',
            'comments'
        ]
        
    def validate_application_id(self, value):
        # Check if application already has an assessment
        if hasattr(value, 'credit_assessment'):
            raise serializers.ValidationError("This application already has an assessment")
        return value

    def create(self, validated_data):
        application = validated_data.pop('application_id')
        analyst = self.context['request'].user
        
        return CreditAssessment.objects.create(
            application=application,
            analyst=analyst,
            status=CreditAssessment.UNDER_REVIEW,  # Default status is Under Review
            **validated_data
        )
