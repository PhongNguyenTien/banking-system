from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.hashers import make_password, check_password
from credit.models.customer_profile import CustomerProfile

class CustomerAccountManager(models.Manager):
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
            
        # Create the user instance with all the extra_fields
        # Don't extract customer_email separately since it's already in extra_fields
        user = self.model(**extra_fields)
        
        # Hash the password
        user.password = make_password(password)
        user.save(using=self._db)
        return user

class CustomerAccount(models.Model):
    customer_email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
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
        
    def set_password(self, raw_password):
        """Set a hashed password"""
        self.password = make_password(raw_password)
        self.save(update_fields=['password'] if self.pk else None)
    
    def check_password(self, raw_password):
        """Check if the provided password matches the stored hash"""
        return check_password(raw_password, self.password)
