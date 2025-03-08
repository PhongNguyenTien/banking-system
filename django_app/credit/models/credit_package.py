from django.db import models

class CreditPackage(models.Model):
    name = models.CharField(max_length=100)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    max_amount = models.DecimalField(max_digits=12, decimal_places=2)
    min_credit_score = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'credit_packages'
