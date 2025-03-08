from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.employee_account import EmployeeLoginView
from .views.customer_account import CustomerLoginView
from rest_framework_simplejwt.views import TokenRefreshView
from .views.employee_account import EmployeeAccountViewSet
from .views.customer_account import CustomerAccountViewSet

router = DefaultRouter()
router.register(r'employees', EmployeeAccountViewSet, basename='employee')
router.register(r'customers', CustomerAccountViewSet, basename='customer')

urlpatterns = [
    path('', include(router.urls)),
    path('employee/login/', EmployeeLoginView.as_view(), name='employee-login'),
    path('customer/login/', CustomerLoginView.as_view(), name='customer-login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]