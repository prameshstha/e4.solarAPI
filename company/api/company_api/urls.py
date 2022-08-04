from django.urls import path

from company.api.company_api.views import CreateListCompany, CompanyEditDeleteView, AddCompanyUser, \
    ChangeAdmin, CompanyCustomerListView, CompanyJobListView, CompanyUserListView, CompanyDetails, \
    RegisterUserInvitation, CompanyAddress, InsertInitialAddress

urlpatterns = [
    path('create-list-company/', CreateListCompany.as_view(), name='create-company'),  # create company
    path('company-details/<int:company_id>/', CompanyDetails.as_view(), name='company-details'),
    path('company-address/<int:company_id>/', CompanyAddress.as_view(), name='company-address'),

    path('company-customer-list/<int:company_id>/', CompanyCustomerListView.as_view(), name='customer-list'),
    path('company-user-list/<int:company_id>/', CompanyUserListView.as_view(), name='customer-list'),
    path('company-job-list/<int:company_id>/', CompanyJobListView.as_view(), name='company-job-list'),
    path('edit-delete/<int:company_id>/', CompanyEditDeleteView.as_view(), name='company-edit-delete'),

    path('add-user/', AddCompanyUser.as_view(), name='add-user'),
    path('register-user-invitation/', RegisterUserInvitation.as_view(), name='register-user-invitation'),
    # path('remove-member/', RemoveCompanyUser.as_view(), name='remove-user'),
    path('change-admin/', ChangeAdmin.as_view(), name='change-admin'),

    # address initial insertion
    path('initial-address/', InsertInitialAddress.as_view(), name='initial-address'),

]