# Generated by Django 4.2.10 on 2024-12-25 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conceptnote', '0035_remove_icn_iregion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activityimpact',
            name='impact_pilot',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='activityimpact',
            name='impact_scaleup',
            field=models.FloatField(blank=True, null=True),
        ),
    ]