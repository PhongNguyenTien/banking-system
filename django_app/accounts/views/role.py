from rest_framework import viewsets, status
from rest_framework.response import Response
from ..models.role import Role
from ..serializers.role import RoleSerializer
from accounts.rbac import RolePermission

class RoleViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing roles.
    Only admin users can perform CRUD operations on roles.
    """
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [RolePermission]

    def destroy(self, request, *args, **kwargs):
        # Check if role is in use before deleting
        instance = self.get_object()
        if instance.employeerole_set.exists():
            return Response(
                {"detail": "Cannot delete role that is assigned to employees."},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().destroy(request, *args, **kwargs) 