from django.contrib import admin

# Register your models here.
from customer_portal.models import CustomerFiles, JobDetails, FileType, InstallationPhotos, PanelSerialNumbers, \
    InverterPhotos, CommonCustomerFile, JobEditHistory, FileFieldSetting

admin.site.register(CustomerFiles)
admin.site.register(JobDetails)
admin.site.register(FileType)
admin.site.register(InstallationPhotos)
admin.site.register(InverterPhotos)
admin.site.register(PanelSerialNumbers)
admin.site.register(CommonCustomerFile)
admin.site.register(JobEditHistory)
admin.site.register(FileFieldSetting)
