# Generated by Django 3.2.9 on 2022-01-12 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rules', '0009_auto_20220112_1939'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hint',
            name='parameter',
            field=models.CharField(choices=[('Salinity', 'Salinity'), ('Temperature', 'Temperature'), ('Carbonate Hardness', 'Carbonate Hardness'), ('Calcium', 'Calcium'), ('Magnesium', 'Magnesium')], max_length=48),
        ),
        migrations.AlterField(
            model_name='rule',
            name='parameter',
            field=models.CharField(choices=[('Salinity', 'Salinity'), ('Temperature', 'Temperature'), ('Carbonate Hardness', 'Carbonate Hardness'), ('Calcium', 'Calcium'), ('Magnesium', 'Magnesium')], default='Temperature', max_length=48),
        ),
    ]