from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.hashers import make_password, check_password
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
        print(">>>> extra_fields: ", extra_fields)
            
        user = self.model(**extra_fields)
        print(">>>>>>>> password: ", password)
        
        # Hash the password exactly like AbstractBaseUser does
        if password:
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
        """Implement the same method as AbstractBaseUser"""
        self.password = make_password(raw_password)
        self._password = raw_password
        self.save(update_fields=['password'])
    
    def check_password(self, raw_password):
        """Implement the same method as AbstractBaseUser"""
        def setter(raw_password):
            self.set_password(raw_password)
            self._password = None
            self.save(update_fields=["password"])
        return check_password(raw_password, self.password, setter)
