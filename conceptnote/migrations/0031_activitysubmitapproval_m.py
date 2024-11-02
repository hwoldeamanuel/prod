# Generated by Django 4.2.10 on 2024-11-02 14:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_admin', '0004_submission_status'),
        ('program', '0006_userroles_is_pacn_finance_approver_and_more'),
        ('conceptnote', '0030_remove_icn_approval_status_final'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivitySubmitApproval_M',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('approval_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('approval_note', models.TextField(blank=True, null=True)),
                ('approval_status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_admin.approvalt_status')),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='conceptnote.activitydocument')),
                ('submit_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='conceptnote.activitysubmit')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='program.userroles')),
            ],
        ),
    ]
