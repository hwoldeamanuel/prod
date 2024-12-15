# Generated by Django 4.2.10 on 2024-12-15 18:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('conceptnote', '0035_remove_icn_iregion'),
        ('report', '0013_activityreport_mel_lead_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='icnreport',
            name='icn',
            field=models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, related_name='icnreport', to='conceptnote.icn'),
        ),
    ]
