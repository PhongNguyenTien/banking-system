from django.db import models
from .credit_application import CreditApplication
from accounts.models import EmployeeAccount
from django.core.validators import MinValueValidator, MaxValueValidator
class CreditAssessment(models.Model):
    UNDER_REVIEW = 1
    APPROVED = 2
    REJECTED = 3
    
    STATUS_CHOICES = [
        (1, 'Under Review'),
        (2, 'Approved'),
        (3, 'Rejected')
    ]
    
    application = models.OneToOneField(
        CreditApplication,
        on_delete=models.CASCADE,
        related_name='credit_assessment'
    )
    analyst = models.ForeignKey(
        EmployeeAccount,
        on_delete=models.CASCADE,
        related_name='assessments',
        null=True,
    )
    risk_score = models.IntegerField(
        validators=[
            MinValueValidator(0, message="Risk score must be at least 0"),
            MaxValueValidator(100, message="Risk score cannot exceed 100")
        ]
    )
    comments = models.TextField(blank=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'credit_assessments'
