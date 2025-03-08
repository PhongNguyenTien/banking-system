from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from ..models import CreditAssessment
from ..serializers.credit_assessment import (
    CreditAssessmentSerializer,
    CreditAssessmentCreateSerializer
)
from ..permissions import CreditAssessmentPermission
from accounts.models import EmployeeAccount

class CreditAssessmentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, CreditAssessmentPermission]
    
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
        print("<<<<<<<<<<<<<<<<<<<<<<", status_value)

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
