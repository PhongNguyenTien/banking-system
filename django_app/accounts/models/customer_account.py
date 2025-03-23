from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from credit.models.customer_profile import CustomerProfile
class CustomerAccountManager(BaseUserManager):
    def create_user(self, password=None, **extra_fields):
        if not password:
            raise ValueError('Password is required')
        
        # Get the customer_profile if it's in extra_fields
        customer_profile = extra_fields.get('customer_profile')
        
        # If customer_email is not in extra_fields but customer_profile exists and has email
        if 'customer_email' not in extra_fields and customer_profile and hasattr(customer_profile, 'email'):
            extra_fields['customer_email'] = customer_profile.email
        
        # Now verify we have an email
        if not extra_fields.get('customer_email'):
            raise ValueError('Email is required (either directly or through customer_profile)')
            
        user = self.model(
            customer_email=extra_fields.get('customer_email'),
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
