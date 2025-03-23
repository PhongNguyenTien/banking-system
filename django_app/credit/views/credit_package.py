from rest_framework import viewsets
from ..models import CreditPackage
from ..serializers.credit_package import CreditPackageSerializer
from credit.rbac import CreditPackagePermission
from common.permissions.base_permissions import has_permission

class CreditPackageViewSet(viewsets.ModelViewSet):
    queryset = CreditPackage.objects.all()
    serializer_class = CreditPackageSerializer
    
    @has_permission(CreditPackagePermission('list'))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @has_permission(CreditPackagePermission('create'))
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @has_permission(CreditPackagePermission('retrieve'))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @has_permission(CreditPackagePermission('update'))
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @has_permission(CreditPackagePermission('destroy'))
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
