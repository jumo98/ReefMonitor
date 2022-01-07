# Generated by Django 3.2.9 on 2022-01-04 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aquariums', '0002_auto_20220102_1338'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='measurement',
            options={'verbose_name': 'Measurement', 'verbose_name_plural': 'Measurements'},
        ),
        migrations.AlterModelOptions(
            name='parameter',
            options={'verbose_name': 'Parameter', 'verbose_name_plural': 'Parameters'},
        ),
        migrations.AlterField(
            model_name='parameter',
            name='name',
            field=models.CharField(choices=[('Salinity', 'Sali'), ('Temperature', 'Temp'), ('Carbonate Hardness', 'Carb'), ('Calcium', 'Calc'), ('Magnesium', 'Magn')], default='Temperature', max_length=48),
        ),
    ]
