from rest_framework import viewsets, status
from rest_framework.response import Response
from ..models.role import Role
from ..serializers.role import RoleSerializer
from common.permissions.base_permissions import has_permission
from accounts.rbac import RolePermission

class RoleViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing roles.
    Only admin users can perform CRUD operations on roles.
    """
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

    @has_permission(RolePermission('list'))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @has_permission(RolePermission('create'))
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @has_permission(RolePermission('retrieve'))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @has_permission(RolePermission('update'))
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @has_permission(RolePermission('destroy'))
    def destroy(self, request, *args, **kwargs):
        # Check if role is in use before deleting
        instance = self.get_object()
        if instance.employeerole_set.exists():
            return Response(
                {"detail": "Cannot delete role that is assigned to employees."},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().destroy(request, *args, **kwargs) 