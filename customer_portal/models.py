import random

from django.db import models

from DarwinSolar.utils import get_filename_ext
from accounts.models import CustomUser, InstallerUser


# Create your models here.
from company.models import Company


def upload_file_path(instance, filename):
    # print('instance', instance.image)
    model_name = instance.__class__.__name__
    company = instance.company
    job_number = instance.job_number
    job = str(job_number)
    print('accd', company)
    try:
        print(instance)
    except Exception as e:
        print(e)
    new_filename = random.randint(1, 3910209312)
    print(model_name, 'jj', job_number, 'ins', instance)

    name, ext = get_filename_ext(filename)
    final_filename = '{name}{new_filename}{ext}'.format(name=name, new_filename=new_filename, ext=ext)
    # companies/company_name/job_number/customer_files/
    # companies/company_name/job_number/job_files/
    return "{companies}/{company}/{job}/{model_name}/{final_filename}".format(
        companies='companies', company=company, model_name=model_name, job=job,
        final_filename=final_filename
    )


class JobDetails(models.Model):
    job_number = models.CharField(max_length=120)
    job_type = models.CharField(max_length=120, blank=True)
    customer_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='customer_job', blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='company_job', blank=True)
    # change address to address_id after we get address database
    street = models.CharField(max_length=120, blank=True)
    city = models.CharField(max_length=120, blank=True)
    postcode = models.CharField(max_length=120, blank=True)
    state = models.CharField(max_length=120, blank=True)
    country = models.CharField(max_length=120, blank=True)
    # change address to address_id after we get address database
    aircon = models.CharField(max_length=120, blank=True)
    no_of_panels = models.CharField(max_length=120, blank=True)
    solar_panel = models.CharField(max_length=120, blank=True)
    system_size = models.CharField(max_length=120, blank=True)
    inverter = models.CharField(max_length=120, blank=True)
    no_of_battery = models.CharField(max_length=120, blank=True)
    hotwater = models.CharField(max_length=120, blank=True)
    installation_date = models.CharField(max_length=120, blank=True)
    back_panel = models.FileField(upload_to=upload_file_path, blank=True)
    front_of_property = models.FileField(upload_to=upload_file_path, blank=True)
    switch_board = models.FileField(upload_to=upload_file_path, blank=True)
    installer_image = models.FileField(upload_to=upload_file_path, blank=True)
    electrician = models.ForeignKey(InstallerUser, on_delete=models.PROTECT, related_name='job_electrician', blank=True, null=True)
    installer = models.ForeignKey(InstallerUser, on_delete=models.PROTECT, related_name='job_installer', blank=True, null=True)
    designer = models.ForeignKey(InstallerUser, on_delete=models.PROTECT, related_name='job_designer', blank=True, null=True)
    nmi = models.CharField(max_length=120, blank=True)
    property_type = models.CharField(max_length=120, blank=True)  # single or multistory
    system_type = models.CharField(max_length=120, blank=True)  # single or three phase
    connection_type = models.CharField(max_length=120, blank=True)  # new, existing(Replacing, Adding)
    system_cost = models.CharField(max_length=255, blank=True, null=True)
    is_financed = models.BooleanField(default=False)
    deposit_paid = models.BooleanField(default=False)
    deposit_amount = models.CharField(max_length=120, blank=True, null=True)
    total_amount_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    quote_sent = models.BooleanField(default=False)
    invoice_sent = models.BooleanField(default=False)
    pv_applied = models.BooleanField(default=False)
    finalized_by = models.ForeignKey(InstallerUser, on_delete=models.PROTECT, related_name='job_finalized_by', blank=True, null=True)
    is_processed = models.BooleanField(default=False)
    processed_by = models.ForeignKey(InstallerUser, on_delete=models.PROTECT, related_name='job_processed_by', blank=True, null=True)
    is_open = models.BooleanField(default=True)

    def __str__(self):
        return str(self.job_number)


class JobEditHistory(models.Model):
    edited_by = models.ForeignKey(InstallerUser, on_delete=models.PROTECT, related_name='edited_by')
    edited_date = models.DateTimeField(auto_now=True)
    edited_model = models.CharField(max_length=255, blank=True, null=True)
    edited_content_old = models.CharField(max_length=255, blank=True, null=True)
    edited_content_new = models.CharField(max_length=255, blank=True, null=True)
    edited_action = models.CharField(max_length=255, blank=True, null=True)


class FileType(models.Model):
    file_type = models.CharField(max_length=255)
    file_details = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='company_file_type')
    to_email = models.EmailField(max_length=255, null=True, blank=True)

    def __str__(self):
        return str(self.file_type)


class FileFieldSetting(models.Model):
    file_type = models.ForeignKey(FileType, on_delete=models.CASCADE, related_name='file_type_field')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='company_file_field')
    file_type_field = models.CharField(max_length=255)
    uploaded_form_field = models.CharField(max_length=255)


def upload_common_file_path(instance, filename):
    # print('instance', instance.image)
    model_name = instance.__class__.__name__
    company = instance.company
    print('accd', company)
    try:
        print(instance)
    except Exception as e:
        print(e)
    new_filename = random.randint(1, 3910209312)
    print(model_name, 'ins', instance)

    name, ext = get_filename_ext(filename)
    final_filename = '{name}{new_filename}{ext}'.format(name=name, new_filename=new_filename, ext=ext)
    # companies/company_name/job_number/customer_files/
    # companies/company_name/job_number/job_files/
    return "{companies}/{company}/{model_name}/{final_filename}".format(
        companies='companies', company=company, model_name=model_name,
        final_filename=final_filename
    )


class CommonCustomerFile(models.Model):
    file_name = models.CharField(max_length=255)
    model_number = models.CharField(max_length=255)
    file_details = models.CharField(max_length=255, null=True, blank=True)
    file = models.FileField(upload_to=upload_common_file_path, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='company_common_file_type')

    def __str__(self):
        return str(self.file_name)


class CustomerFiles(models.Model):
    customer_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='customer_files')
    job_number = models.ForeignKey(JobDetails, on_delete=models.CASCADE, related_name='job_number_files', blank=True)
    file_name = models.CharField(max_length=120, blank=True)
    file = models.FileField(upload_to=upload_file_path, blank=True)
    file_type = models.ForeignKey('FileType', on_delete=models.CASCADE, related_name='file_type_file', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='company_files', blank=True, null=True)

    def __str__(self):
        return str(self.file_type) + ' - ' + str(self.job_number) + ' - ' + str(self.file_name)


class PanelSerialNumbers(models.Model):
    job_number = models.ForeignKey(JobDetails, on_delete=models.CASCADE, related_name='job_panels_serials')
    panel_serial_number = models.CharField(max_length=255)
    psn_image = models.CharField(max_length=255)
    psn_location_latitude = models.CharField(max_length=255)
    psn_location_longitude = models.CharField(max_length=255)
    psn_timestamp = models.CharField(max_length=255)

    def __str__(self):
        return str(self.job_number)


# Installation image category
class InstallationImageName(models.Model):
    installation_image_name = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    def __str__(self):
        return str(self.installation_image_name)


class InstallationPhotos(models.Model):
    job_number = models.ForeignKey(JobDetails, on_delete=models.CASCADE, related_name='job_number_installation_image')
    installation_image_name = models.ForeignKey(InstallationImageName, on_delete=models.CASCADE, related_name='installation_image')
    installation_image_location_latitude = models.CharField(max_length=255)
    installation_image_location_longitude = models.CharField(max_length=255)
    installation_image_timestamp = models.CharField(max_length=255)
    installation_image = models.FileField(upload_to=upload_file_path, blank=True)

    def __str__(self):
        return str(self.job_number)


class InverterSerialNumber(models.Model):
    job_number = models.ForeignKey(JobDetails, on_delete=models.CASCADE, related_name='job_inverter_serial')
    inverter_serial = models.CharField(max_length=120)
    inverter_serial_image = models.FileField(upload_to=upload_file_path, blank=True)
    inverter_location_latitude = models.CharField(max_length=255)
    inverter_location_longitude = models.CharField(max_length=255)
    inverter_timestamp = models.CharField(max_length=255)

    def __str__(self):
        return str(self.job_number)


class InverterPhotos(models.Model):
    job_number = models.ForeignKey(JobDetails, on_delete=models.CASCADE, related_name='job_inverter')
    image = models.FileField(upload_to=upload_file_path, blank=True)
    image_desc = models.CharField(max_length=120)

    def __str__(self):
        return str(self.job_number)

