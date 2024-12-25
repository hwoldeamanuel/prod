# Generated by Django 4.2.10 on 2024-12-25 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conceptnote', '0037_alter_impact_impact_pilot_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='impact',
            name='unit',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Numeric-Int'), (2, 'Percentage'), (3, 'Other'), (4, 'Numeric_Decimal')], null=True),
        ),
    ]