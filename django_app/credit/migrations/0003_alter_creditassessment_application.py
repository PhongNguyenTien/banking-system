# Generated by Django 3.2.25 on 2025-02-19 15:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('credit', '0002_alter_creditapplication_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='creditassessment',
            name='application',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='credit_assessment', to='credit.creditapplication'),
        ),
    ]
