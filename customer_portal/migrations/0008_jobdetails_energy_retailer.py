# Generated by Django 4.1 on 2022-08-24 01:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customer_portal', '0007_alter_filetype_to_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobdetails',
            name='energy_retailer',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, related_name='energy_retailer_job', to='customer_portal.electricityretailers'),
            preserve_default=False,
        ),
    ]
