# Generated by Django 4.2.10 on 2024-03-22 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conceptnote', '0007_icn_icn_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='acn_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]