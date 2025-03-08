from django.db import models
from .customer_profile import CustomerProfile
from .credit_package import CreditPackage

class CreditApplication(models.Model):
    customer_profile = models.ForeignKey(
        CustomerProfile,
        on_delete=models.CASCADE,
        related_name='credit_applications'
    )
    credit_package = models.ForeignKey(
        CreditPackage,
        on_delete=models.CASCADE,
        related_name='applications'
    )
    amount_requested = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'credit_applications'

    @property
    def status(self):
        """
        Return the status based on the associated credit assessment.
        If no assessment exists, the application is considered 'Pending'.
        """
        if hasattr(self, 'credit_assessment'):
            assessment = self.credit_assessment
            if assessment.status == 1:  # Under Review
                return 'Under Review'
            elif assessment.status == 2:  # Approved
                return 'Approved'
            elif assessment.status == 3:  # Rejected
                return 'Rejected'
        return 'Pending'
