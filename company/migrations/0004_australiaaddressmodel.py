# Generated by Django 3.2.13 on 2022-08-02 23:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0003_delete_australiaaddressmodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='AustraliaAddressModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hash', models.CharField(max_length=255, unique=True)),
                ('unit', models.CharField(max_length=255)),
                ('number', models.CharField(max_length=255)),
                ('street', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('district', models.CharField(max_length=255)),
                ('state', models.CharField(max_length=255)),
                ('country', models.CharField(default='Australia', max_length=255)),
                ('postcode', models.CharField(max_length=255)),
                ('address_original_id', models.CharField(max_length=255, unique=True)),
                ('longitude', models.CharField(max_length=255)),
                ('latitude', models.CharField(max_length=255)),
            ],
        ),
    ]