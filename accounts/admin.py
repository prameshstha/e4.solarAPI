from django.contrib import admin

# Register your models here.
from accounts.models import CustomUser, InstallerUser, InstallerToken

admin.site.register(CustomUser)
admin.site.register(InstallerUser)
admin.site.register(InstallerToken)