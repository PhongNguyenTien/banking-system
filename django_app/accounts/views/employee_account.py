from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..models import EmployeeAccount
from ..permissions import EmployeeAccountPermission
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

from ..serializers.employee_account import EmployeeAccountCreateSerializer, EmployeeAccountSerializer
from ..serializers.login import EmployeeLoginSerializer


class EmployeeAccountViewSet(viewsets.ModelViewSet):
    queryset = EmployeeAccount.objects.all()
    permission_classes = [IsAuthenticated, EmployeeAccountPermission]

    def get_serializer_class(self):
        if self.action == 'create':
            return EmployeeAccountCreateSerializer
        return EmployeeAccountSerializer

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
                        'role': user.role,
                        'employee_code': user.employee_code
                    }
                })
            return Response(
                {'error': 'Invalid credentials'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
