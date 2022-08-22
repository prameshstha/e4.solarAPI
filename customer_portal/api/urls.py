from django.urls import path

from company.api.installer_api.views import CommonCustomerFileView
from customer_portal.api.views import AllCustomerFileView, CustomerFileView, SearchJob, CustomerJob, \
    AllFileTypeView, EditDeleteFileTypeView, CustomerJobEditByUser, EditCustomerAllDetails, ZapTest

urlpatterns = [
    path('file-list/', AllCustomerFileView.as_view(), name='file-list'),
    # path('file-upload/', AddCustomerFiles.as_view(), name='file-upload'),

    path('file-types/<int:company_id>/', AllFileTypeView.as_view(), name='file-types'),
    path('common-file/<int:company_id>/', CommonCustomerFileView.as_view(), name='common-user-file'),

    path('edit-delete-file-types/<int:pk>/', EditDeleteFileTypeView.as_view(), name='edit-delete-file-types'),
    path('job-search/<int:customer_id>/', SearchJob.as_view(), name='job-search'),
    path('<int:customer_id>/', CustomerJob.as_view(), name='customer-job'),
    path('by-user/<int:customer_id>/', CustomerJobEditByUser.as_view(), name='customer-job-user'),

    path('update-customer-all-details/<str:is_finalized>/', EditCustomerAllDetails.as_view(), name='customer-job'),

    path('<int:customer_id>/customer-files/', CustomerFileView.as_view(), name='file-search'),
    path('zap/', ZapTest.as_view(), name='file-search'),


]
