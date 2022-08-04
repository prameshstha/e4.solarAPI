from django.urls import path

from company.api.app.views import SearchJobByJobNumber

urlpatterns = [
    path('search-job/<str:job_number>/', SearchJobByJobNumber.as_view(), name='one-job'),
    # path('completed-job/', AddCustomerFiles.as_view(), name='file-upload'),


]
