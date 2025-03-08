from django.urls import path, include
from rest_framework.routers import DefaultRouter

from credit.views.credit_application import CreditApplicationViewSet
from credit.views.credit_assessment import CreditAssessmentViewSet
from credit.views.credit_package import CreditPackageViewSet
from credit.views.customer_profile import CustomerProfileViewSet

router = DefaultRouter()
router.register(r'packages', CreditPackageViewSet, basename='credit-package')
router.register(r'applications', CreditApplicationViewSet, basename='credit-application')
router.register(r'assessments', CreditAssessmentViewSet, basename='credit-assessment')
router.register(r'customers', CustomerProfileViewSet, basename='customer-profile')

urlpatterns = [
    path('', include(router.urls)),
] 