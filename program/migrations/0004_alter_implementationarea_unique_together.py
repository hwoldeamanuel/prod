# Generated by Django 4.2.10 on 2024-09-29 21:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_admin', '0004_submission_status'),
        ('program', '0003_program_portfolio'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='implementationarea',
            unique_together={('program', 'woreda')},
        ),
    ]