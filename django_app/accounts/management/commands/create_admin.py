from django.core.management.base import BaseCommand
from accounts.models.employee_account import EmployeeAccount
from accounts.models.employee_information import EmployeeInformation
from accounts.models.role import Role
from accounts.models.employee_role import EmployeeRole
from accounts.utils.employee_code_generator import generate_employee_code

class Command(BaseCommand):
    help = 'Creates an admin user'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, help='Admin username')
        parser.add_argument('--password', type=str, help='Admin password')
        parser.add_argument('--full_name', type=str, help='Admin full name')
        parser.add_argument('--age', type=int, help='Admin age')
        parser.add_argument('--phone', type=str, help='Admin phone number')
        parser.add_argument('--address', type=str, help='Admin address')

    def handle(self, *args, **options):
        username = options.get('username') or 'admin'
        password = options.get('password') or 'admin123'
        full_name = options.get('full_name') or 'System Administrator'
        age = options.get('age') or 30
        phone = options.get('phone') or '123-456-7890'
        address = options.get('address') or 'Admin Address'

        # Check if admin role exists, create if not
        admin_role, created = Role.objects.get_or_create(
            id=Role.ADMIN,
            defaults={'name': 'Admin'}
        )

        # Create employee account
        admin = EmployeeAccount.objects.create_user(
            username=username,
            password=password
        )

        # Generate employee code
        employee_code = generate_employee_code(Role.ADMIN, EmployeeInformation)

        # Create employee information
        EmployeeInformation.objects.create(
            employee=admin,
            full_name=full_name,
            age=age,
            phone_number=phone,
            address=address,
            employee_code=employee_code
        )

        # Assign admin role
        EmployeeRole.objects.create(
            employee=admin,
            role=admin_role
        )

        self.stdout.write(self.style.SUCCESS(
            f'Admin user created successfully with username: {username}'
        )) 