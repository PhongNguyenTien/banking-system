from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from ..models import CreditPackage
from ..serializers.credit_package import CreditPackageSerializer
from ..permissions import CreditPackagePermission

class CreditPackageViewSet(viewsets.ModelViewSet):
    queryset = CreditPackage.objects.all()
    serializer_class = CreditPackageSerializer
    permission_classes = [IsAuthenticated, CreditPackagePermission]
