# Generated by Django 4.2.10 on 2024-10-31 16:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('conceptnote', '0029_icn_approval_status_final'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='icn',
            name='approval_status_final',
        ),
    ]
