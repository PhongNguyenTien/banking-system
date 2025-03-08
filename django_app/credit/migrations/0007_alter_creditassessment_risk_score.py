# Generated by Django 3.2.25 on 2025-03-02 09:28

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('credit', '0006_remove_customerprofile_is_approved'),
    ]

    operations = [
        migrations.AlterField(
            model_name='creditassessment',
            name='risk_score',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0, message='Risk score must be at least 0'), django.core.validators.MaxValueValidator(100, message='Risk score cannot exceed 100')]),
        ),
    ]
