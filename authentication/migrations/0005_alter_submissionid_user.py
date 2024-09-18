# Generated by Django 4.2.16 on 2024-09-17 11:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_webhookresponse'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submissionid',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_submission_id', to=settings.AUTH_USER_MODEL),
        ),
    ]
