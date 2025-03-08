# Generated by Django 3.2.25 on 2025-02-16 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_employeeaccount_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeeaccount',
            name='role',
            field=models.IntegerField(choices=[(4, 'Transaction Officer'), (2, 'Credit Analysis'), (3, 'Credit Manager'), (1, 'Admin'), (5, 'Audit')]),
        ),
    ]
