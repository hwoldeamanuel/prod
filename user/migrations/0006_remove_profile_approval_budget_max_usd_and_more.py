# Generated by Django 4.2.10 on 2024-11-12 18:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_profile_approval_budget_max_usd_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='approval_budget_max_usd',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='approval_budget_min_usd',
        ),
    ]
