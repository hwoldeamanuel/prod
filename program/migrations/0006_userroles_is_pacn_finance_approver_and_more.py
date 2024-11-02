# Generated by Django 4.2.10 on 2024-10-29 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('program', '0005_userroles_is_pcn_mel_approver'),
    ]

    operations = [
        migrations.AddField(
            model_name='userroles',
            name='is_pacn_finance_approver',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userroles',
            name='is_pacn_initiator',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userroles',
            name='is_pacn_mel_approver',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userroles',
            name='is_pacn_program_approver',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userroles',
            name='is_pacn_technical_approver',
            field=models.BooleanField(default=False),
        ),
    ]
