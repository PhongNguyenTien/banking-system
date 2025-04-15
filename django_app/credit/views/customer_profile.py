from rest_framework import viewsets
from ..models import CustomerProfile
from ..serializers.customer_profile import CustomerProfileSerializer
from credit.rbac import CustomerProfilePermission

class CustomerProfileViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerProfileSerializer
    queryset = CustomerProfile.objects.all()
    permission_classes = [CustomerProfilePermission]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'customer_profile'):
            return CustomerProfile.objects.filter(id=user.customer_profile.id)
        return CustomerProfile.objects.all()

