# Generated by Django 3.2.13 on 2022-08-02 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AustraliaAddressModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hash', models.CharField(max_length=255)),
                ('unit', models.CharField(max_length=255)),
                ('number', models.CharField(max_length=255)),
                ('street', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('district', models.CharField(max_length=255)),
                ('state', models.CharField(max_length=255)),
                ('postcode', models.CharField(max_length=255)),
                ('add_original_id', models.CharField(max_length=255)),
                ('longitude', models.CharField(max_length=255)),
                ('latitude', models.CharField(max_length=255)),
            ],
        ),
    ]