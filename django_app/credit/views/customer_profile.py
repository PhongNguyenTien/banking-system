from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from ..models import CustomerProfile
from ..serializers.customer_profile import CustomerProfileSerializer
from ..permissions import CustomerProfilePermission
from accounts.models import EmployeeAccount

class CustomerProfileViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerProfileSerializer
    permission_classes = [IsAuthenticated, CustomerProfilePermission]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'customer_profile'):
            return CustomerProfile.objects.filter(id=user.customer_profile.id)
        return CustomerProfile.objects.all()
