from django.apps import AppConfig


class CustomerPortalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'customer_portal'

    # to check customer files uploaded / added by Pramesh Shrestha
    # def ready(self):
    #     print('ready called here')
    #     from customer_portal.check_files_uploaded import file_checker
    #     file_checker.check_files()
