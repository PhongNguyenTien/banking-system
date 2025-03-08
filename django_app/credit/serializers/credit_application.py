from rest_framework import serializers
from ..models import CreditApplication, CustomerProfile, CreditPackage
from .customer_profile import CustomerProfileSerializer
from .credit_package import CreditPackageSerializer

class CreditApplicationSerializer(serializers.ModelSerializer):
    customer_profile = CustomerProfileSerializer(read_only=True)
    credit_package = CreditPackageSerializer(read_only=True)
    customer_profile_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomerProfile.objects.all(),
        source='customer_profile',
        write_only=True,
        required=False
    )
    credit_package_id = serializers.PrimaryKeyRelatedField(
        queryset=CreditPackage.objects.all(),
        source='credit_package',
        write_only=True,
        required=False
    )
    status = serializers.CharField(read_only=True)

    class Meta:
        model = CreditApplication
        fields = [
            'id',
            'customer_profile',
            'credit_package',
            'customer_profile_id',
            'credit_package_id',
            'amount_requested',
            'status',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'status']


class CreditApplicationCreateSerializer(serializers.ModelSerializer):
    customer_profile_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomerProfile.objects.all()
    )
    credit_package_id = serializers.PrimaryKeyRelatedField(
        queryset=CreditPackage.objects.all()
    )

    class Meta:
        model = CreditApplication
        fields = [
            'customer_profile_id',
            'credit_package_id',
            'amount_requested'
        ]

    def create(self, validated_data):
        customer_profile = validated_data.pop('customer_profile_id')
        credit_package = validated_data.pop('credit_package_id')
        return CreditApplication.objects.create(
            customer_profile=customer_profile,
            credit_package=credit_package,
            **validated_data
        )
