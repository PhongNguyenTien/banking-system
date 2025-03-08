# Generated by Django 3.2.25 on 2025-02-28 16:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('credit', '0003_alter_creditassessment_application'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='creditapplication',
            name='status',
        ),
        migrations.AddField(
            model_name='creditassessment',
            name='status',
            field=models.IntegerField(choices=[(1, 'Under Review'), (2, 'Approved'), (3, 'Rejected')], default=1),
        ),
        migrations.AlterField(
            model_name='creditassessment',
            name='analyst',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assessments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='creditassessment',
            name='comments',
            field=models.TextField(blank=True),
        ),
    ]
