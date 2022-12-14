# Generated by Django 3.2.13 on 2022-07-01 04:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DCHubDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dc_48_current1', models.FloatField()),
                ('dc_48_current2', models.FloatField()),
                ('dc_48_current3', models.FloatField()),
                ('dc_48_current4', models.FloatField()),
                ('dc_48_current5', models.FloatField()),
                ('dc_48_voltage1', models.FloatField()),
                ('dc_48_voltage2', models.FloatField()),
                ('pv1_voltage', models.FloatField()),
                ('pv1_current', models.FloatField()),
                ('bms_voltage', models.FloatField()),
                ('bms_current', models.FloatField()),
                ('battery_capacity', models.FloatField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
