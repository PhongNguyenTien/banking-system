from rest_framework import viewsets
from ..models import CreditPackage
from ..serializers.credit_package import CreditPackageSerializer
from credit.rbac import CreditPackagePermission

class CreditPackageViewSet(viewsets.ModelViewSet):
    queryset = CreditPackage.objects.all()
    serializer_class = CreditPackageSerializer
    permission_classes = [CreditPackagePermission]

