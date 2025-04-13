from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from ..serializers.employee_role import EmployeeRoleAssignSerializer
from ..models.employee_role import EmployeeRole
from common.permissions.base_permissions import has_permission
from accounts.rbac import RoleAssignmentPermission

class EmployeeRoleAssignView(APIView):
    """
    API endpoint for assigning roles to employees.
    Only admin users can assign roles.
    """
    serializer_class = EmployeeRoleAssignSerializer
    
    @has_permission(RoleAssignmentPermission('assign'))
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            role_assignment = serializer.save()
            return Response({
                "message": "Role assigned successfully",
                "employee_id": role_assignment.employee.id,
                "role_id": role_assignment.role.id,
                "role_name": role_assignment.role.name
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
