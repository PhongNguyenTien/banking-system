from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from ..models import CreditApplication
from ..serializers.credit_application import (
    CreditApplicationSerializer,
    CreditApplicationCreateSerializer
)
from ..permissions import CreditApplicationPermission
from accounts.models import EmployeeAccount

class CreditApplicationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, CreditApplicationPermission]
    
    def get_queryset(self):
        user = self.request.user
        if user.role in [EmployeeAccount.TRANSACTION_OFFICER, EmployeeAccount.CREDIT_ANALYST, EmployeeAccount.CREDIT_MANAGER]:
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

        # Credit analysts should not be able to update applications
        if request.user.role == EmployeeAccount.CREDIT_ANALYST:
            return Response(
                {"detail": "Credit analysts cannot update applications"},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)
        