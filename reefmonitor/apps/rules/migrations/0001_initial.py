# Generated by Django 3.2.9 on 2022-01-03 18:01

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('aquariums', '0002_auto_20220102_1338'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rule',
            fields=[
                ('id', models.CharField(blank=True, default=uuid.uuid4, max_length=100, primary_key=True, serialize=False, unique=True)),
                ('value', models.FloatField()),
                ('type', models.CharField(choices=[('minimum', 'Min'), ('maximal', 'Max')], default='minimum', max_length=48)),
                ('parameter', models.CharField(choices=[('salinity', 'Sali'), ('temperature', 'Temp'), ('carbonate', 'Carb'), ('calcium', 'Calc'), ('magnesium', 'Magn')], default='temperature', max_length=48)),
                ('aquarium', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aquariums.aquarium')),
            ],
            options={
                'verbose_name': 'Rule',
                'verbose_name_plural': 'Rules',
            },
        ),
    ]
