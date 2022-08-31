from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path, include

from accounts.api.views import CustomerListView, CustomerEditDeleteView, Login, Logout, RegistrationView, \
    ChangePasswordView, UpdateNmiFromLink, GetLoggedInUser, AllRetailers, AllRetailerForms, EditDeleteAllRetailersView, EditDeleteAllRetailersForms, TestPdf

urlpatterns = [
    path('login/', Login.as_view(), name='login-token'),  # post request only - login
    path('logout/', Logout.as_view(), name='logout-token'),  # post request only
    path('register/', RegistrationView.as_view(), name='register-token'),  # post request only
    path('user-list/', CustomerListView.as_view(), name='user-list'),
    path('get-loggedin-user/<int:pk>/', GetLoggedInUser.as_view(), name='get-loggedin-user'),
    path('user-edit-delete/<int:pk>/<int:company_id>/', CustomerEditDeleteView.as_view(), name='user-edit-delete'),
    # Change Password
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),  # patch request

    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),

    # path('test-form-email/', TestFormEmail.as_view(), name='test-form-email'),

    path('update-nmi/', UpdateNmiFromLink.as_view(), name='update-nmi'),

    path('all-retailers/', AllRetailers.as_view(), name='all-retailers'),
    path('edit-delete-retailers/<int:pk>/', EditDeleteAllRetailersView.as_view(), name='edit-delete-retailers'),
    path('all-retailer-forms/<int:retailer_id>/', AllRetailerForms.as_view(), name='all-retailer-forms'),
    path('edit-delete-retailer-form/<int:pk>/', EditDeleteAllRetailersForms.as_view(), name='edit-delete-retailer-form'),


    path('test-pdf/', TestPdf.as_view(), name='test-form-email'),
    # password_reset/confirm/ to change password form api front end
    # path('change-request/', ChangePasswordView.as_view(), name='change-password'),  # patch request
]