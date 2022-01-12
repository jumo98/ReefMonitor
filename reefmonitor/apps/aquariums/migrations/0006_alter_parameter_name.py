# Generated by Django 3.2.9 on 2022-01-12 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aquariums', '0005_alter_parameter_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parameter',
            name='name',
            field=models.CharField(choices=[('Salinity', 'Sali'), ('Temperature', 'Temp'), ('Carbonate Hardness', 'Carb'), ('Calcium', 'Calc'), ('Magnesium', 'Magn')], default='Temperature', max_length=48),
        ),
    ]
