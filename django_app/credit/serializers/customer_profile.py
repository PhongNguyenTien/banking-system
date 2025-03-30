from rest_framework import serializers
from ..models import CustomerProfile

class CustomerProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CustomerProfile
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'annual_income',
            'credit_score',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def validate_annual_income(self, value):
        if value <= 0:
            raise serializers.ValidationError("Annual income must be greater than 0")
        return value

    def validate_phone_number(self, value):
        # Add basic phone number validation
        if not value.isdigit() or len(value) < 10:
            raise serializers.ValidationError("Please enter a valid phone number")
        return value