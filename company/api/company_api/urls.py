from django.urls import path

from company.api.company_api.views import RegisterCompany, CompanyEditDeleteView, AddCompanyUser, \
    ChangeAdmin, CompanyCustomerListView, CompanyJobListView, CompanyUserListView, CompanyDetails, \
    RegisterUserInvitation, CompanyAddress, SearchAddressView, InsertInitialAddress, ActivateCompany

urlpatterns = [
    path('register-company/', RegisterCompany.as_view(), name='create-company'),  # create company
    path('activate-company/', ActivateCompany.as_view(), name='activate-company'),  # Activate company
    path('resend-activate-company/', ActivateCompany.as_view(), name='resend-activate-company'),  # resend Activate company

    path('company-details/<int:company_id>/', CompanyDetails.as_view(), name='company-details'),
    path('company-address/<int:company_id>/', CompanyAddress.as_view(), name='company-address'),

    path('company-customer-list/<int:company_id>/', CompanyCustomerListView.as_view(), name='customer-list'),
    path('company-user-list/<int:company_id>/<str:is_installer>/', CompanyUserListView.as_view(), name='users-list'),
    path('company-job-list/<int:company_id>/', CompanyJobListView.as_view(), name='company-job-list'),
    path('edit-delete/<int:company_id>/', CompanyEditDeleteView.as_view(), name='company-edit-delete'),

    path('add-user/', AddCompanyUser.as_view(), name='add-user'),
    path('register-user-invitation/', RegisterUserInvitation.as_view(), name='register-user-invitation'),
    # path('remove-member/', RemoveCompanyUser.as_view(), name='remove-user'),
    path('change-admin/', ChangeAdmin.as_view(), name='change-admin'),

    # address initial insertion
    # path('initial-address/', InsertInitialAddress.as_view(), name='initial-address'),
    path('initial-address/', SearchAddressView.as_view(), name='search-address'),

]