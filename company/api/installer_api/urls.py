from django.urls import path

from company.api.installer_api.views import InstallerListView, InstallerEditDeleteView, Login, Logout, \
    ChangePasswordView, InstallerPasswordReset, ResetPasswordAPI, CustomerListView, CustomerEditDeleteView, \
    AllFileTypeView, AddCustomerFiles, CommonFileView, CommonCustomerFileView, PvApplicationView, EmailDocuments

urlpatterns = [
    path('login/', Login.as_view(), name='installer-login'),  # post request only - login
    path('logout/', Logout.as_view(), name='installer-logout-token'),  # post request only
    # path('register/', RegistrationView.as_view(), name='installer-register-token'),
    path('installer-list/', InstallerListView.as_view(), name='installer-list'),
    path('installer-edit-delete/<int:pk>', InstallerEditDeleteView.as_view(), name='installer-edit-delete'),

    path('file-upload/', AddCustomerFiles.as_view(), name='file-upload'),

    path('pv-application/<int:company_id>/', PvApplicationView.as_view(), name='pv-application'),
    path('send-documents-email/', EmailDocuments.as_view(), name='send-documents-email'),

    # path('customer-list/', CustomerListView.as_view(), name='customer-list'),

    path('customer-edit-delete/<int:pk>/<int:company_id>/', CustomerEditDeleteView.as_view(), name='customer-edit-delete'),
    path('file-types/<int:company>/', AllFileTypeView.as_view(), name='file-types'),

    path('common-file/<int:company>/', CommonFileView.as_view(), name='common-file'),
    path('all-common-file/<int:company>/', CommonCustomerFileView.as_view(), name='common-file'),
    # path('common-file-edit-delete/<int:company>/', EditDeleteCommonFileView.as_view(), name='edit-common-file'),

    # Change Password
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),  # patch request

    path('password_reset/', InstallerPasswordReset.as_view(), name='installer-password-reset'),
    path('password-reset/confirm/', ResetPasswordAPI.as_view(), name='installer-password-reset-token'),

    # path('password_reset/', include('django_rest_passwordreset.urls', namespace='installer-password-reset')),
]