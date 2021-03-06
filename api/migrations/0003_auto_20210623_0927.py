# Generated by Django 3.2.3 on 2021-06-23 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_user_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='otp',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='otp_send_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='otp_varification',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='password_reset_otp_verification',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
