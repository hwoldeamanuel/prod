# Generated by Django 4.2.10 on 2024-11-01 16:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('program', '0006_userroles_is_pacn_finance_approver_and_more'),
        ('app_admin', '0004_submission_status'),
        ('report', '0011_alter_activityreport_cs_currency_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='icnreport',
            name='mel_lead',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='irmel_lead', to='program.userroles'),
        ),
        migrations.CreateModel(
            name='IcnReportSubmitApproval_M',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('approval_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('approval_note', models.TextField(blank=True, null=True)),
                ('approval_status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_admin.approvalt_status')),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='report.icnreportdocument')),
                ('submit_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='report.icnreportsubmit')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='program.userroles')),
            ],
        ),
    ]