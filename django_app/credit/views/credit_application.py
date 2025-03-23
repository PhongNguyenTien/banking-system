from rest_framework import viewsets, status
from rest_framework.response import Response
from ..models import CreditApplication
from ..serializers.credit_application import (
    CreditApplicationSerializer,
    CreditApplicationCreateSerializer
)
from accounts.models import EmployeeAccount
from common.permissions.base_permissions import has_permission
from credit.rbac import CreditApplicationPermission


class CreditApplicationViewSet(viewsets.ModelViewSet):
    
    def get_queryset(self):
        user = self.request.user
        if user.role in [EmployeeAccount.TRANSACTION_OFFICER, EmployeeAccount.CREDIT_ANALYST, EmployeeAccount.CREDIT_MANAGER, EmployeeAccount.AUDIT]:
            return CreditApplication.objects.all()
        return CreditApplication.objects.filter(
            customer_profile__account=user
        )

    def get_serializer_class(self):
        if self.action == 'create':
            return CreditApplicationCreateSerializer
        return CreditApplicationSerializer
    
    @has_permission(CreditApplicationPermission('list'))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @has_permission(CreditApplicationPermission('create'))
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    @has_permission(CreditApplicationPermission('retrieve'))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @has_permission(CreditApplicationPermission('update'))
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
    
    @has_permission(CreditApplicationPermission('destroy'))
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
    
        