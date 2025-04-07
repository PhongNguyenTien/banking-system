from rest_framework import viewsets, status
from rest_framework.response import Response
from accounts.models import CustomerAccount
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

from ..serializers.customer_account import CustomerAccountCreateSerializer, CustomerAccountSerializer
from ..serializers.login import CustomerLoginSerializer
from common.permissions.base_permissions import has_permission
from accounts.rbac import CustomerAccountPermission

class CustomerAccountViewSet(viewsets.ModelViewSet):
    queryset = CustomerAccount.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'create':
            return CustomerAccountCreateSerializer
        return CustomerAccountSerializer
    
    @has_permission(CustomerAccountPermission('list'))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @has_permission(CustomerAccountPermission('create'))
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @has_permission(CustomerAccountPermission('retrieve'))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @has_permission(CustomerAccountPermission('update'))
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @has_permission(CustomerAccountPermission('destroy'))
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class CustomerLoginView(APIView):
    permission_classes = []
    serializer_class = CustomerLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            
            try:
                user = CustomerAccount.objects.get(customer_email=email)
                if user.check_password(password) and user.is_active:
                    refresh = RefreshToken.for_user(user)
                    return Response({
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                        'user': {
                            'id': user.id,
                            'email': user.customer_email,
                            'profile': {
                                'first_name': user.customer_profile.first_name,
                                'last_name': user.customer_profile.last_name
                            }
                        }
                    })
            except CustomerAccount.DoesNotExist:
                pass
            
            return Response(
                {'error': 'Invalid credentials'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
