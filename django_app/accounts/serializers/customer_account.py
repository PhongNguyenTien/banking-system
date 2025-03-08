from rest_framework import serializers
from ..models.customer_account import CustomerAccount

from credit.serializers.customer_profile import CustomerProfileSerializer
from credit.models.customer_profile import CustomerProfile


class CustomerAccountCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    profile = CustomerProfileSerializer()

    class Meta:
        model = CustomerAccount
        fields = ['customer_email', 'password', 'profile']

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        profile = CustomerProfile.objects.create(**profile_data)
        validated_data['customer_profile'] = profile
        return CustomerAccount.objects.create_user(**validated_data)