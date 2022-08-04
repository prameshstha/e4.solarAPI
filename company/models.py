import binascii
import os
from datetime import datetime
from django.db import models

# Create your models here.
from DarwinSolar.utils import get_filename_ext
from accounts.models import CustomUser, InstallerUser


def upload_file_path(instance, filename):
    # print('instance', instance.image)
    model_name = instance.__class__.__name__
    new_filename = datetime.now()
    company = instance.company_name
    # print(model_name, 'jj', 'ins', instance)
    name, ext = get_filename_ext(filename)
    # companies/company_name/job_number/customer_files/
    # companies/company_name/images/
    final_filename = '{name}{new_filename}{ext}'.format(name=name, new_filename=new_filename, ext=ext)

    return "{companies}/{company}/images/{final_filename}".format(
        companies='companies', company=company,
        final_filename=final_filename)


class Company(models.Model):
    company_name = models.CharField(max_length=255)
    company_logo = models.ImageField(upload_to=upload_file_path, blank=True, null=True)
    # company_address = models.ForeignKey(AddressModel, on_delete=models.CASCADE, related_name='company_address')
    # billing_address = models.ForeignKey(AddressModel, on_delete=models.CASCADE, related_name='billing_address')
    company_admin = models.ManyToManyField(InstallerUser, related_name='company_admin')
    company_users = models.ManyToManyField(InstallerUser, related_name='company_member', blank=True)
    company_customers = models.ManyToManyField(CustomUser, related_name='company_customers', blank=True)
    company_statues = models.CharField(max_length=255)
    company_phone = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.company_name)


class AustraliaAddressModel(models.Model):
    hash = models.CharField(max_length=255, unique=True)
    unit = models.CharField(max_length=255)
    number = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    district = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    country = models.CharField(max_length=255, default='Australia')
    postcode = models.CharField(max_length=255)
    address_original_id = models.CharField(max_length=255, unique=True)
    longitude = models.CharField(max_length=255)
    latitude = models.CharField(max_length=255)

    def __str__(self):
        return str(self.unit) + '/' + str(self.street) + ' ' + str(self.city) + ' ' + str(self.state) + ' ' + str(self.country) + ' ' + str(self.postcode)



ADDRESS_TYPES = (
    ('billing', 'Billing Address'),
    ('company_address', 'Company Address'),
)


class AddressModel(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='company_address')
    unit = models.CharField(max_length=255)
    street = models.CharField(max_length=120, blank=True)
    city = models.CharField(max_length=120, blank=True)
    postcode = models.CharField(max_length=120, blank=True)
    state = models.CharField(max_length=120, blank=True)
    country = models.CharField(max_length=120, blank=True)
    address_type = models.CharField(max_length=120, choices=ADDRESS_TYPES)

    def __str__(self):
        return str(self.address_type) + ' => ' + str(self.unit) + '/' + str(self.street) + ' ' + str(self.city) + ' ' + str(self.state) + ' ' + str(self.country) + ' ' + str(self.postcode)


class Subscription(models.Model):
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='company_id_sub')
    current_period_start = models.DateTimeField()
    current_period_end = models.DateTimeField()
    is_auto_renew = models.BooleanField(default=True)
    canceled_at = models.DateTimeField()
    ended_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.current_period_start) + ' to ' + str(self.current_period_end)


class BillingDetails(models.Model):
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='company_id')
    subscription_id = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name='subscription_id')
    billing_period_start = models.DateTimeField()
    billing_period_end = models.DateTimeField()
    invoice_number = models.CharField(max_length=255)
    invoice_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.billing_period_start) + ' to ' + str(self.billing_period_end)


class InstallerInvitation(models.Model):
    """
    The InstallerUser invitation token model.
    """
    key = models.CharField("Key", max_length=40, primary_key=True)
    email = models.EmailField(max_length=255, unique=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='invitation_company')
    invitation_created = models.DateTimeField(auto_now_add=True)
    invitation_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "InstallerInvitation"
        verbose_name_plural = "InstallerInvitation"

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(InstallerInvitation, self).save(*args, **kwargs)

    def generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.key
