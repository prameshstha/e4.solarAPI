from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path, include

from accounts.api.views import CustomerListView, CustomerEditDeleteView, Login, Logout, RegistrationView, \
    ChangePasswordView

urlpatterns = [
    path('login/', Login.as_view(), name='login-token'),  # post request only - login
    path('logout/', Logout.as_view(), name='logout-token'),  # post request only
    path('register/', RegistrationView.as_view(), name='register-token'),  # post request only
    path('user-list/', CustomerListView.as_view(), name='user-list'),
    path('user-edit-delete/<int:pk>/<int:company_id>/', CustomerEditDeleteView.as_view(), name='user-edit-delete'),
    # Change Password
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),  # patch request

    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    # password_reset/confirm/ to change password form api front end
    # path('change-request/', ChangePasswordView.as_view(), name='change-password'),  # patch request
]