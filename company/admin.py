from django.contrib import admin

# Register your models here.
from company.models import Company, Subscription, BillingDetails, InstallerInvitation, AddressModel, \
    AustraliaAddressModel

admin.site.register(Company)
admin.site.register(Subscription)
admin.site.register(BillingDetails)
admin.site.register(InstallerInvitation)
admin.site.register(AddressModel)
admin.site.register(AustraliaAddressModel)