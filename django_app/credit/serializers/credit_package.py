from rest_framework import serializers
from ..models import CreditPackage

class CreditPackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditPackage
        fields = [
            'name',
            'interest_rate',
            'max_amount',
            'min_credit_score',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def validate_interest_rate(self, value):
        if value < 0 or value > 100:
            raise serializers.ValidationError("Interest rate must be between 0 and 100")
        return value

    def validate_max_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Maximum amount must be greater than 0")
        return value
