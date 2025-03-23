from rest_framework import viewsets
from ..models import CustomerProfile
from ..serializers.customer_profile import CustomerProfileSerializer
from credit.rbac import CustomerProfilePermission
from common.permissions.base_permissions import has_permission

class CustomerProfileViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerProfileSerializer
    queryset = CustomerProfile.objects.all()

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'customer_profile'):
            return CustomerProfile.objects.filter(id=user.customer_profile.id)
        return CustomerProfile.objects.all()
    
    @has_permission(CustomerProfilePermission('list'))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @has_permission(CustomerProfilePermission('create'))
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @has_permission(CustomerProfilePermission('retrieve'))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @has_permission(CustomerProfilePermission('update'))
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @has_permission(CustomerProfilePermission('destroy'))
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
