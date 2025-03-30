from rest_framework import viewsets, status
from rest_framework.response import Response
from ..models import EmployeeAccount
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

from ..serializers.employee_account import EmployeeAccountCreateSerializer, EmployeeAccountSerializer
from ..serializers.login import EmployeeLoginSerializer
from common.permissions.base_permissions import has_permission
from accounts.rbac import EmployeeAccountPermission

class EmployeeAccountViewSet(viewsets.ModelViewSet):
    queryset = EmployeeAccount.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return EmployeeAccountCreateSerializer
        return EmployeeAccountSerializer

    @has_permission(EmployeeAccountPermission('list'))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @has_permission(EmployeeAccountPermission('create'))
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @has_permission(EmployeeAccountPermission('retrieve'))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @has_permission(EmployeeAccountPermission('update'))
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @has_permission(EmployeeAccountPermission('destroy'))
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class EmployeeLoginView(APIView):
    permission_classes = []
    serializer_class = EmployeeLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password']
            )
            
            if user and user.is_active:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'employee_code': user.information.employee_code,
                    }
                })
            return Response(
                {'error': 'Invalid credentials'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
