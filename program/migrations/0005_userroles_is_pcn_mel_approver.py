# Generated by Django 4.2.10 on 2024-10-29 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('program', '0004_alter_implementationarea_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='userroles',
            name='is_pcn_mel_approver',
            field=models.BooleanField(default=False),
        ),
    ]