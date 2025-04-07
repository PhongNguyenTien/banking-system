from rest_framework import serializers
from ..models.customer_account import CustomerAccount

from credit.serializers.customer_profile import CustomerProfileSerializer
from credit.models.customer_profile import CustomerProfile

class CustomerAccountSerializer(serializers.ModelSerializer):
    """
    Serializer for returning CustomerAccount information.
    This serializer is meant for read operations, not for creating accounts.
    """
    profile = CustomerProfileSerializer(source='customer_profile', read_only=True)
    email = serializers.EmailField(source='customer_email', read_only=True)
    
    class Meta:
        model = CustomerAccount
        fields = [
            'id',
            'email',
            'profile',
            'is_active',
            'created_at',
            'updated_at'
        ]
        read_only_fields = fields


class CustomerAccountCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    profile_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomerProfile.objects.all(),
        source='customer_profile',
        write_only=True,
        required=False
    )

    class Meta:
        model = CustomerAccount
        fields = ['password', 'profile_id']
        extra_kwargs = {'password': {'write_only': True}}
        
    def validate(self, data):
        profile_data = data.get('profile')
        profile_id = data.get('customer_profile')
        
        if not profile_data and not profile_id:
            raise serializers.ValidationError("Either profile or profile_id must be provided")
        
        return data

    def create(self, validated_data):
        profile_data = validated_data.pop('profile', None)
        password = validated_data.pop('password')
        
        if profile_data:
            profile = CustomerProfile.objects.create(**profile_data)
            validated_data['customer_profile'] = profile
        else:
            profile = validated_data.get('customer_profile')
        
        if 'customer_email' not in validated_data or not validated_data['customer_email']:
            validated_data['customer_email'] = profile.email
        print(">>>> validated_data: ", validated_data)
        
        return CustomerAccount.objects.create_user(
            password=password,
            **validated_data
        )
    
    def to_representation(self, instance):
        """
        Control what gets returned after creation
        """
        ret = super().to_representation(instance)
        ret['message'] = "Customer account created successfully"
        return ret