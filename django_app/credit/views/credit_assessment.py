from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from ..models import CreditAssessment
from ..serializers.credit_assessment import (
    CreditAssessmentSerializer,
    CreditAssessmentCreateSerializer
)
from accounts.models import EmployeeAccount
from common.permissions.base_permissions import has_permission
from credit.rbac import CreditAssessmentPermission

class CreditAssessmentViewSet(viewsets.ModelViewSet):
    
    def get_queryset(self):
        user = self.request.user
        if user.role == EmployeeAccount.CREDIT_ANALYST:
            return CreditAssessment.objects.filter(analyst=user)
        elif user.role == EmployeeAccount.CREDIT_MANAGER:
            return CreditAssessment.objects.all()
        return CreditAssessment.objects.none()

    def get_serializer_class(self):
        if self.action == 'create':
            return CreditAssessmentCreateSerializer
        return CreditAssessmentSerializer
    
    @has_permission(CreditAssessmentPermission('list'))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @has_permission(CreditAssessmentPermission('create'))
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
            
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @has_permission(CreditAssessmentPermission('retrieve'))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @has_permission(CreditAssessmentPermission('destroy'))
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
    @has_permission(CreditAssessmentPermission('update'))
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        # Prevent status updates through the regular update method
        if 'status' in request.data:
            if request.user.role == EmployeeAccount.CREDIT_MANAGER:
                return Response(
                    {"detail": "Credit managers should use the /update_status/ endpoint to update status"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            else:
                return Response(
                    {"detail": "Only credit managers can update the status field"},
                    status=status.HTTP_403_FORBIDDEN
                )
        
        # For credit analysts, allow updating other fields
        if request.user.role == EmployeeAccount.CREDIT_ANALYST:
            request_data = request.data
        else:
            # Other roles shouldn't be able to update assessments
            return Response(
                {"detail": "You do not have permission to update this assessment"},
                status=status.HTTP_403_FORBIDDEN
            )
            
        serializer = self.get_serializer(instance, data=request_data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response(serializer.data)
        
    @has_permission(CreditAssessmentPermission('update_status'))
    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        """
        Update the status of a credit assessment (approve or reject).
        Only credit managers can update the status.
        """
        # Permission check is handled by the permission class
        assessment = self.get_object()
        
        # Check if assessment is in a state that can be updated
        if assessment.status != CreditAssessment.UNDER_REVIEW:
            return Response(
                {"detail": "Only assessments under review can have their status updated"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # Get the new status value
        status_value = request.data.get("status")
        
        # Validate that status_value is present
        if status_value is None:
            return Response(
                {"detail": "Status field is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # Try to convert to integer
        try:
            status_value = int(status_value)
        except (ValueError, TypeError):
            return Response(
                {"detail": "Status must be an integer value"},
                status=status.HTTP_400_BAD_REQUEST
            )
        # Validate the status value

        if status_value not in [CreditAssessment.APPROVED, CreditAssessment.REJECTED]:
            return Response(
                {"detail": f"Status must be either {CreditAssessment.APPROVED} (Approved) or {CreditAssessment.REJECTED} (Rejected)"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # Update assessment status
        assessment.status = status_value
        assessment.save()
        
        status_text = "approved" if status_value == CreditAssessment.APPROVED else "rejected"
        return Response(
            {
                "detail": f"Assessment has been {status_text}",
                "assessment": CreditAssessmentSerializer(assessment).data
            },
            status=status.HTTP_200_OK
        )
