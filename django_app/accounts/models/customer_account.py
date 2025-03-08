from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from credit.models.customer_profile import CustomerProfile
class CustomerAccountManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        user = self.model(
            customer_email=email,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

class CustomerAccount(AbstractBaseUser):
    customer_email = models.EmailField(unique=True)
    customer_profile = models.OneToOneField(
        CustomerProfile,
        on_delete=models.CASCADE,
        related_name='account'
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomerAccountManager()

    USERNAME_FIELD = 'customer_email'

    class Meta:
        db_table = 'customer_accounts'
