# Generated by Django 4.2.10 on 2024-11-12 20:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('program', '0007_userroles_apprval_budget_max_usd_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userroles',
            old_name='apprval_budget_max_usd',
            new_name='approval_budget_max_usd',
        ),
        migrations.RenameField(
            model_name='userroles',
            old_name='apprval_budget_min_usd',
            new_name='approval_budget_min_usd',
        ),
    ]
