# Generated by Django 4.2.10 on 2025-01-11 21:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0012_remove_submitapproval_s_submission_status_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='requestsubmit',
            name='submission_status',
        ),
    ]