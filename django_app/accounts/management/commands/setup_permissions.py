# from django.core.management.base import BaseCommand
# from django.contrib.auth.models import Group, Permission
# from django.contrib.contenttypes.models import ContentType
# from accounts.models.user_account import UserAccount
# from credit.models import (
#     CustomerProfile, CreditPackage, CreditApplication, CreditAssessment
# )

# class Command(BaseCommand):
#     help = 'Sets up groups and permissions for banking system'

#     def handle(self, *args, **options):
#         # Create groups (roles)
#         admin_group, _ = Group.objects.get_or_create(name='Admin')
#         credit_analyst_group, _ = Group.objects.get_or_create(name='Credit Analyst')
#         credit_manager_group, _ = Group.objects.get_or_create(name='Credit Manager')
#         transaction_officer_group, _ = Group.objects.get_or_create(name='Transaction Officer')
#         audit_group, _ = Group.objects.get_or_create(name='Audit')
        
#         # Create customer groups (roles)
#         basic_customer_group, _ = Group.objects.get_or_create(name='Basic Customer')
#         premium_customer_group, _ = Group.objects.get_or_create(name='Premium Customer')
#         vip_customer_group, _ = Group.objects.get_or_create(name='VIP Customer')
        
#         # Get content types
#         user_ct = ContentType.objects.get_for_model(UserAccount)
#         customer_profile_ct = ContentType.objects.get_for_model(CustomerProfile)
#         credit_package_ct = ContentType.objects.get_for_model(CreditPackage)
#         credit_app_ct = ContentType.objects.get_for_model(CreditApplication)
#         credit_assessment_ct = ContentType.objects.get_for_model(CreditAssessment)
        
#         # Define Admin permissions (full access)
#         admin_permissions = Permission.objects.filter(
#             content_type__in=[user_ct, customer_profile_ct, credit_package_ct, 
#                                credit_app_ct, credit_assessment_ct]
#         )
#         admin_group.permissions.set(admin_permissions)
        
#         # Credit Analyst permissions
#         analyst_perms = [
#             # Can view customer profiles
#             Permission.objects.get(codename='view_customerprofile', content_type=customer_profile_ct),
#             # Can view/add/change credit assessments
#             Permission.objects.get(codename='view_creditassessment', content_type=credit_assessment_ct),
#             Permission.objects.get(codename='add_creditassessment', content_type=credit_assessment_ct),
#             Permission.objects.get(codename='change_creditassessment', content_type=credit_assessment_ct),
#             # Can view credit applications
#             Permission.objects.get(codename='view_creditapplication', content_type=credit_app_ct),
#         ]
#         credit_analyst_group.permissions.set(analyst_perms)
        
#         # Credit Manager permissions
#         manager_perms = [
#             # Can view/change credit assessments and applications
#             Permission.objects.get(codename='view_creditassessment', content_type=credit_assessment_ct),
#             Permission.objects.get(codename='change_creditassessment', content_type=credit_assessment_ct),
#             Permission.objects.get(codename='view_creditapplication', content_type=credit_app_ct),
#             Permission.objects.get(codename='change_creditapplication', content_type=credit_app_ct),
#             # Can view customer profiles
#             Permission.objects.get(codename='view_customerprofile', content_type=customer_profile_ct),
#             # Can view/change credit packages
#             Permission.objects.get(codename='view_creditpackage', content_type=credit_package_ct),
#             Permission.objects.get(codename='change_creditpackage', content_type=credit_package_ct),
#         ]
#         credit_manager_group.permissions.set(manager_perms)
        
#         # Transaction Officer permissions
#         transaction_perms = [
#             # Can view/add/change customer profiles
#             Permission.objects.get(codename='view_customerprofile', content_type=customer_profile_ct),
#             Permission.objects.get(codename='add_customerprofile', content_type=customer_profile_ct),
#             Permission.objects.get(codename='change_customerprofile', content_type=customer_profile_ct),
#             # Can view/add credit applications
#             Permission.objects.get(codename='view_creditapplication', content_type=credit_app_ct),
#             Permission.objects.get(codename='add_creditapplication', content_type=credit_app_ct),
#             # Can view credit packages
#             Permission.objects.get(codename='view_creditpackage', content_type=credit_package_ct),
#         ]
#         transaction_officer_group.permissions.set(transaction_perms)
        
#         # Audit permissions
#         audit_perms = [
#             # View-only access to everything
#             Permission.objects.get(codename='view_customerprofile', content_type=customer_profile_ct),
#             Permission.objects.get(codename='view_creditpackage', content_type=credit_package_ct),
#             Permission.objects.get(codename='view_creditapplication', content_type=credit_app_ct),
#             Permission.objects.get(codename='view_creditassessment', content_type=credit_assessment_ct),
#         ]
#         audit_group.permissions.set(audit_perms)
        
#         # Customer permissions setup
#         # Basic Customer permissions
#         basic_customer_perms = [
#             # Can view their own profile and standard credit packages
#             Permission.objects.get(codename='view_customerprofile', content_type=customer_profile_ct),
#             Permission.objects.get(codename='view_creditpackage', content_type=credit_package_ct),
#             # Can create and view their own applications
#             Permission.objects.get(codename='add_creditapplication', content_type=credit_app_ct),
#             Permission.objects.get(codename='view_creditapplication', content_type=credit_app_ct),
#         ]
#         basic_customer_group.permissions.set(basic_customer_perms)
        
#         # Premium Customer permissions (everything Basic has plus more)
#         premium_customer_perms = basic_customer_perms + [
#             # Premium customers might get access to premium credit packages
#             # or additional features
#         ]
#         premium_customer_group.permissions.set(premium_customer_perms)
        
#         # VIP Customer permissions (highest tier)
#         vip_customer_perms = premium_customer_perms + [
#             # VIPs might get even more privileges
#         ]
#         vip_customer_group.permissions.set(vip_customer_perms)
        
#         self.stdout.write(self.style.SUCCESS('Successfully set up groups and permissions')) 