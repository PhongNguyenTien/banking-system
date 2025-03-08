from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..models import CustomerAccount
from ..permissions import CustomerAccountPermission
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

from ..serializers.customer_account import CustomerAccountCreateSerializer
from ..serializers.login import CustomerLoginSerializer


class CustomerAccountViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, CustomerAccountPermission]
    serializer_class = CustomerAccountCreateSerializer

    def get_queryset(self):
        return CustomerAccount.objects.all()

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
            user = authenticate(
                username=serializer.validated_data['email'],
                password=serializer.validated_data['password']
            )
            
            if user and user.is_active:
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
            return Response(
                {'error': 'Invalid credentials'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
