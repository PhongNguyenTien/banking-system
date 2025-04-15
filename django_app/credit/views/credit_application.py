from rest_framework import viewsets, status
from rest_framework.response import Response
from ..models import CreditApplication
from ..serializers.credit_application import (
    CreditApplicationSerializer,
    CreditApplicationCreateSerializer
)
from credit.rbac import CreditApplicationPermission
from accounts.models.role import Role

class CreditApplicationViewSet(viewsets.ModelViewSet):
    permission_classes = [CreditApplicationPermission]
    
    def get_queryset(self):
        user = self.request.user
        if user.roles.filter(role__id__in=[Role.TRANSACTION_OFFICER, Role.CREDIT_ANALYST, Role.CREDIT_MANAGER, Role.AUDITOR]).exists():
            return CreditApplication.objects.all()
        return CreditApplication.objects.filter(
            customer_profile__account=user
        )

    def get_serializer_class(self):
        if self.action == 'create':
            return CreditApplicationCreateSerializer
        return CreditApplicationSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)
    