import threading
import threading

from django.contrib.auth import logout
from django.contrib.auth.hashers import check_password
from django.core.mail import EmailMultiAlternatives
from django.forms import model_to_dict
from django.template.loader import render_to_string
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from DarwinSolar.utils import EmailThread
from accounts.api.serializer import CustomUserSerializer, RegistrationSerializer, AllCustomUserSerializer, \
    ChangePasswordSerializer, CustomUserSerializer1
from accounts.models import CustomUser
from company.models import Company
from customer_portal.api.serializer import CustomerFilesSerializer, JobDetailsSerializer


class CustomerListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.all()
    serializer_class = AllCustomUserSerializer


class CustomerEditDeleteView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # print(self.kwargs)
        customer_id = self.kwargs['pk']

        queryset = CustomUser.objects.filter(id=customer_id)
        return queryset
    serializer_class = CustomUserSerializer


class Login(APIView):
    def post(self, request):
        # serializer = LoginSerializer(data=request.data)
        print(request.data)
        email = request.data['email']
        password = request.data['password']

        if email and password:
            try:
                # Try to find a user matching your username
                user = CustomUser.objects.get(email=email)
                pwd_valid = check_password(password, user.password)
                print(pwd_valid)
                #  Check the password is the reverse of the username
                # something wrong here need to check asap
                if pwd_valid:
                    # Yes? return the Django user object
                    token = Token.objects.get_or_create(user=user)
                    # change according to the needs
                    # if customer are client single company

                    # company = Company.objects.filter(company_customers=user).first()
                    # if customer are client of multiple company
                    company = Company.objects.filter(company_customers=user).values()
                    user_dict = (model_to_dict(user))
                    user_dict.pop('last_login')
                    user_dict.pop('date_joined')
                    user_dict.pop('groups')
                    user_dict.pop('user_permissions')
                    user_dict.pop('password')
                    user_dict['token'] = str(token[0])
                    user_dict['company'] = company  # if customer are client of multiple company
                    # user_dict['company_name'] = company.company_name
                    return Response(user_dict, 200)
                else:
                    # No? return None - triggers default login failed
                    return Response({'Error': 'Email or Password wrong'}, 403)
            except CustomUser.DoesNotExist:
                # No user was found, return None - triggers default login failed
                return Response({'Error': 'User Does not exist'}, 404)


def modify_input_for_multiple_files(company_id, customer_crm_id, first_name, last_name, phone, email,
                                    street, city, postcode, state, country, job_number, solar_panel,
                                    system_size, inverter, no_of_battery, hotwater, aircon,
                                    no_of_panels, installation_date):
    password = 'darwinsolar@2022'
    customer_details = {'customer_crm_id': customer_crm_id, 'first_name': first_name, 'last_name': last_name,
                        'phone': phone, 'email': email, 'street': street, 'city': city, 'postcode': postcode,
                        'state': state, 'country': country, 'password': password}
    # company = Company.objects.filter(id=company_id).first()
    job_details = {'company': company_id, 'street': street, 'city': city, 'postcode': postcode, 'state': state, 'country': country,
                   'job_number': job_number, 'aircon': aircon, 'no_of_panels': no_of_panels, 'solar_panel': solar_panel,
                   'system_size': system_size, 'inverter': inverter, 'no_of_battery': no_of_battery,
                   'hotwater': hotwater, 'installation_date': installation_date}
    customer_files = {'customer_crm_id': customer_crm_id, 'job_number': job_number}
    return customer_details, job_details, customer_files


class RegistrationView(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        print(request.data)
        req = request.data
        # dummy data
        reqs = {'company_id': 3, 'customer_id': '12009051', 'first_name': 'pramesh', 'last_name': 'SolarTest', 'phone': '+610424011797',
                'job_number': 'DSD1172', 'email': 'pramesh11172@gmail.com', 'street': '1/35 De Latour Street',
                'city': 'Coconut Grove', 'postcode': '0810', 'state': 'NT', 'country': 'Australia',
                'solar_panel': 'REC',
                'system_size': '9900', 'inverter': 'Soltaro AIO 10kW Inverter + 10kW Battery', 'no_of_battery': '2x',
                'hotwater': '12 Panel;270L', 'aircon': 'Deye 5kW', 'no_of_panels': '30',
                'installation_date': 'Nov 06 2021'}
        company_id = req.get('company_id', '')  # this is most required!!!
        customer_crm_id = req.get('customer_id', '')
        first_name = req.get('first_name', '')
        last_name = req.get('last_name', '')
        phone = req.get('phone', '')
        email = req.get('email', '')
        street = req.get('street', '')
        city = req.get('city', '')
        postcode = req.get('postcode', '')
        state = req.get('state', '')
        country = req.get('country', '')
        job_number = req.get('job_number', '')
        solar_panel = req.get('solar_panel', '')
        system_size = req.get('system_size', '')
        inverter = req.get('inverter', '')
        no_of_battery = req.get('no_of_battery', '')
        hotwater = req.get('hotwater', '')
        aircon = req.get('aircon', '')
        no_of_panels = req.get('no_of_panels', '')
        installation_date = req.get('installation_date', '')
        try:
            customer_already_exists = CustomUser.objects.get(email=email)
            return Response('Customer with email "{}" already exists'.format(email), 403)
        except CustomUser.DoesNotExist:
            customer_details, job_details, customer_files = modify_input_for_multiple_files(company_id, customer_crm_id,
                                                                                            first_name,
                                                                                            last_name,
                                                                                            phone, email,
                                                                                            street, city, postcode,
                                                                                            state,
                                                                                            country,
                                                                                            job_number, solar_panel,
                                                                                            system_size, inverter,
                                                                                            no_of_battery, hotwater,
                                                                                            aircon,
                                                                                            int(no_of_panels),
                                                                                            installation_date)
            account_serializer = RegistrationSerializer(data=customer_details)
            data = {}
            if account_serializer.is_valid():
                user = account_serializer.save()
                token = Token.objects.create(user=user)

                print(user)
                # email user with email and password
                # ask user to change password
                link = "https://e4.solar"
                customer = user.first_name
                if user.first_name == '':
                    customer = user.email
                merge_data = {
                    'customer': customer,
                    'customer_email': user.email,
                    'link': link,  # change in production level
                    'password': 'darwinsolar@2022'
                }

                email_subject = "Welcome to Darwin Solar portal."
                email_html_body = render_to_string("welcome.html", merge_data)
                from_email = "reception@darwinsolar.com.au"
                to_email = [user.email]
                send_email = EmailMultiAlternatives(
                    email_subject,
                    email_html_body,
                    from_email,
                    to_email,

                )
                send_email.attach_alternative(email_html_body, "text/html")

                if user:
                    # to send email faster
                    # EmailThread(send_email).start() # paused
                    job_details['customer_id'] = user.id
                    job_details_serializer = JobDetailsSerializer(data=job_details)
                    print(job_details_serializer.is_valid(), job_details_serializer.errors)
                    print('user added')
                    if job_details_serializer.is_valid():
                        try:
                            job = job_details_serializer.save()
                            # job.customer_id = user
                            # job.save()
                            print('job', job)
                        except Exception as e:
                            print('err', e)
                    company = Company.objects.get(id=company_id)
                    company.company_customers.add(user)

                    print(job_details_serializer.errors)

                    # remove this line
                    # if customer_files_serializer.is_valid():
                    #     files = customer_files_serializer.save()
                    #     print('files', files)
                    # print(customer_files_serializer.errors)

                return Response('User created', 200)
            else:
                data = account_serializer.errors
                print(data)
            return Response(data, 403)


class Logout(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print(request.user)
        print(request.data)
        logout(request)
        return Response({'message': 'User Logged out'})


class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """

    serializer_class = ChangePasswordSerializer
    model = CustomUser
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        print('changepassowerddaf', request.data)
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response("Bad credentials!", 400)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()

            return Response('Password updated successfully!', 200)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
