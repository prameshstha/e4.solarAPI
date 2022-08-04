from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.views import APIView

from accounts.api.serializer import AllCustomUserSerializer

from DarwinSolar.utils import EmailThread
from accounts.models import InstallerUser, InstallerToken
from company.api.app.views import del_s3_file
from company.api.installer_api.authentication import InstallerTokenAuthentication
from company.api.company_api.serializer import CompanySerializer, AddressSerializer, AustraliaAddressSerializer
from company.api.installer_api.serializer import InstallerUserSerializer, RegistrationInstallerUserSerializer
from company.models import Company, InstallerInvitation, AddressModel, AustraliaAddressModel
from customer_portal.models import JobDetails


class CreateListCompany(generics.ListCreateAPIView):
    authentication_classes = [InstallerTokenAuthentication]
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class CompanyEditDeleteView(APIView):
    authentication_classes = [InstallerTokenAuthentication]

    def patch(self, request, **kwargs):
        print(request.data)
        has_file = request.data['hasFile']
        company_id = kwargs['company_id']
        billing_add = request.data.get('billing_add')
        company_add = request.data.get('company_add')
        if has_file:
            comp = json.loads(company_add) if company_add != 'undefined' else None
            bill_add = json.loads(billing_add) if billing_add != 'undefined' else None
            print('yes')
        else:
            comp = company_add
            bill_add = billing_add
        if bill_add is not None:
            try:
                b_address = AddressModel.objects.get(id=bill_add.get('id'))
                bill_address_serializer = AddressSerializer(b_address, data=billing_add, partial=True)
                print(bill_address_serializer.is_valid())
                if bill_address_serializer.is_valid():
                    bill_address_serializer.save()
            except AddressModel.DoesNotExist:
                bill_add['address_type'] = 'billing'
                bill_add['company'] = company_id
                bill_address_serializer = AddressSerializer(data=bill_add)
                print('bill is valid', bill_address_serializer.is_valid(), bill_address_serializer.errors)
                bill_address_serializer.save()
        if comp is not None:
            try:
                c_address = AddressModel.objects.get(id=comp.get('id'))
                company_address_serializer = AddressSerializer(c_address, data=comp, partial=True)
                print(company_address_serializer.is_valid())
                if company_address_serializer.is_valid():
                    company_address_serializer.save()
            except AddressModel.DoesNotExist:
                company_add['address_type'] = 'company_address'
                company_add['company'] = company_id
                company_address_serializer = AddressSerializer(data=company_add)
                print('company is valid', company_address_serializer.is_valid(), company_address_serializer.errors)
                company_address_serializer.save()
        if has_file:
            serializer = CompanySerializer(data=request.data)
            print(serializer.is_valid(), serializer.errors)
            try:
                logo_already = Company.objects.get(id=company_id)
                print(logo_already.company_logo)
                try:
                    del_s3_file(str(logo_already.company_logo))
                except Exception as er:
                    print(er)
                fileSerializer = CompanySerializer(logo_already, data=request.data, partial=True)
                # print(fileSerializer.is_valid())
                # print(fileSerializer.errors)
                if fileSerializer.is_valid():
                    # self.perform_update()
                    fileSerializer.save()
                return Response('Edited', 200)
            except Company.DoesNotExist:
                print('No file found')
                return Response('Not Edited', 401)
            # job_numb = request.data['job_numb']
        else:
            del request.data['company_logo']
            company = Company.objects.get(id=company_id)
            ser = CompanySerializer(company, data=request.data, partial=True)
            print('after removing', ser.is_valid())
            if ser.is_valid():
                ser.save()
                return Response('success', 200)
            else:
                return Response('Please refresh and try again', 400)


class CompanyDetails(generics.ListAPIView):
    authentication_classes = [InstallerTokenAuthentication]

    def get_queryset(self):
        company_id = self.kwargs['company_id']
        print(self.kwargs)
        queryset = Company.objects.filter(id=company_id)
        print(queryset)
        return queryset

    serializer_class = CompanySerializer


class CompanyAddress(generics.ListAPIView):
    authentication_classes = [InstallerTokenAuthentication]

    def get_queryset(self):
        company_id = self.kwargs['company_id']
        company = Company.objects.filter(id=company_id).first()
        queryset = AddressModel.objects.filter(company=company)
        return queryset
    serializer_class = AddressSerializer


class CompanyJobListView(APIView):
    authentication_classes = [InstallerTokenAuthentication]

    def get(self, request,  *args, **kwargs):
        print(request.data,  args, kwargs)
        company_id = kwargs['company_id']
        # queryset = JobDetails.objects.filter(company=company_id).select_related('customer_id')
        # ab = JobDetails.objects.select_related('company').all()
        queryset = JobDetails.objects.filter(company=company_id).values()
        # print(queryset.query)
        # print(model_to_dict(queryset))

        print(queryset[0]['company_id'])

        cu = Company.objects.get(id=queryset[0]['company_id'])
        company_customers = cu.company_customers.all().values()
        print(cu.company_customers.all())
        # print(queryset.query())
        # k = json.loads(serialize('json', queryset))
        # k = json.dumps(list(queryset), default=str)
        # company_cust = json.dumps(list(company_customers), default=str)
        # k = serializers.serialize(queryset, many=True)
        # company_cust = serializers.serialize(company_customers, many=True)
        # company_cust = json.loads(serialize('json', company_customers))
        # print(k)
        return Response({'jobs': queryset, 'company_cust': company_customers}, 200)


# class CompanyJobListView(generics.ListCreateAPIView):
#     authentication_classes = [InstallerTokenAuthentication]
#     serializer_class = JobDetailsSerializer1
#
#     def get_queryset(self):
#         company_id = self.kwargs['company_id']
#         print(company_id)
#
#         # queryset = JobDetails.objects.filter(company=company_id).select_related('customer_id')
#         queryset = JobDetails.objects.prefetch_related('customer_id')
#         # print(queryset.query, company_id)
#         # for a in queryset:
#         #     a.query()
#         return queryset


class CompanyCustomerListView(generics.ListCreateAPIView):
    authentication_classes = [InstallerTokenAuthentication]

    def get_queryset(self):
        company_id = self.kwargs['company_id']

        queryset = Company.objects.get(id=company_id)
        company_customers = queryset.company_customers.all()

        # print(queryset.company_customers.all())
        # a = CustomUserSerializer(data=company_customers)
        return company_customers

    serializer_class = AllCustomUserSerializer


class CompanyUserListView(generics.ListCreateAPIView):
    authentication_classes = [InstallerTokenAuthentication]

    def get_queryset(self):
        company_id = self.kwargs['company_id']

        queryset = Company.objects.get(id=company_id)
        company_users = queryset.company_users.all()

        # print(queryset.company_customers.all())
        # a = CustomUserSerializer(data=company_customers)
        return company_users

    serializer_class = InstallerUserSerializer


# Add user to company or send user invitation
class AddCompanyUser(APIView):
    authentication_classes = [InstallerTokenAuthentication]

    def post(self, request, **kwargs):
        print(request.data, kwargs)
        user_email = request.data['user_email']
        company_id = request.data['company_id']
        company = Company.objects.get(id=company_id)

        try:
            user = InstallerUser.objects.get(email=user_email)
            if user in company.company_users.all():
                data = 'This user already exists this company.'
                return Response(data, 201)
            else:
                # write code to add user in the company
                company.company_users.add(user)
                data = 'New user added'
                return Response(data, 200)

        except InstallerUser.DoesNotExist:
            # 'This email address does not have account in this app. Do you want to invite them?'
            data = 'This email address does not have an account. Email invitation sent ' + user_email
            # send invitation email to the user
            domain = 'https://e4.solar/register-new-user'
            domain = 'http://localhost:3000/register-new-user'

            try:
                tok = InstallerInvitation.objects.get(email=user_email, company=company)
                data = 'Invitation already sent to ' + '"' + user_email + '". Please check email.'
                print(tok.key)
                return Response(data, 200)
            except InstallerInvitation.DoesNotExist:
                encoded_email = urlsafe_base64_encode(force_bytes(user_email))
                encoded_pk = urlsafe_base64_encode(force_bytes(company.pk))
                token = InstallerInvitation.objects.create(email=user_email, company=company)
                link = "?token=" + token.key + '&compy=' + encoded_pk + '&em=' + encoded_email
                register_url = domain+link
                print(register_url)

                merge_data = {
                    'user_email': user_email,
                    'company': company.company_name,
                    'register_url': register_url  # change in production level
                }
                email_subject = "You are invited to join {company}. Click the link below to join.".format(company=str(company))
                email_html_body = render_to_string("user_invitation.html", merge_data)
                from_email = "reception@darwinsolar.com.au"
                to_email = [user_email]
                send_email = EmailMultiAlternatives(
                    email_subject,
                    email_html_body,
                    from_email,
                    to_email,
                )
                send_email.attach_alternative(email_html_body, "text/html")
                EmailThread(send_email).start()  # to send email faster

                return Response(data, 200)
            except InstallerUser.MultipleObjectsReturned:
                data = 'Something is wrong. Please try again.'
                return Response(data, 201)


# Register Installer user after invitation
class RegisterUserInvitation(APIView):
    # authentication_classes = [InstallerTokenAuthentication]

    def post(self, request):
        print(request.data)
        encoded_pk = request.data['encodePk']
        print('test', encoded_pk)
        token = request.data['token']
        email = request.data['email']
        try:
            user_exist = InstallerUser.objects.get(email=email)
            return Response('User already registered!')
        except InstallerUser.DoesNotExist:
            try:
                company_id = urlsafe_base64_decode(encoded_pk).decode()
            except Exception as e:
                print(e)
                return Response('Invalid company invitation link.', 201)
            try:
                company = Company.objects.get(id=company_id)
            except Company.DoesNotExist:
                return Response('Unavailable company invitation link.', 201)
            try:
                installer_invitation = InstallerInvitation.objects.get(key=token, company=company)
                serializer = RegistrationInstallerUserSerializer(data=request.data)
                print(serializer.is_valid(), serializer.errors)
                if serializer.is_valid():
                    # write code to save serializer and send email
                    user = serializer.save()
                    print(user)
                    token = InstallerToken.objects.get_or_create(user=user)
                    # user created email

                    link = "e4.solar"
                    # print(sender, "sender", instance, "instance", reset_password_token, "reset_password_token",
                    #       reset_password_token.user.email)
                    print(link)
                    print(user.first_name, user.email)
                    customer = user.first_name
                    if user.first_name == '':
                        customer = user.email
                    merge_data = {
                        'customer': customer,
                        'customer_email': user.email,
                        'company_name': company.company_name,
                        'link': link,  # change in production level
                    }

                    email_subject = "Welcome to " + company.company_name
                    email_html_body = render_to_string("welcome_installer.html", merge_data)
                    from_email = "reception@darwinsolar.com.au"
                    to_email = [user.email]
                    send_email = EmailMultiAlternatives(
                        email_subject,
                        email_html_body,
                        from_email,
                        to_email,

                    )
                    send_email.attach_alternative(email_html_body, "text/html")
                    EmailThread(send_email).start()  # to send email faster
                    data = 'User successfully created!'
                    return Response(data, 200)

            except InstallerInvitation.DoesNotExist:
                return Response('Invalid invitation link.', 201)

            print('installer_invitation', installer_invitation, 'emailll', installer_invitation.email)
            print(str(serializer.errors))

        return Response('Something is wrong', 201)


class ChangeAdmin(APIView):
    authentication_classes = [InstallerTokenAuthentication]

    def post(self, request):
        data = {}
        print('change admin', request.data)
        company_id = request.data['company_id']
        user_id = request.data['user_id']
        action = request.data['action']
        try:
            user = InstallerUser.objects.get(id=user_id)
        except InstallerUser.DoesNotExist:
            return Response('User does not exists')
        company = Company.objects.get(id=company_id)
        print(user, company, '-==-=================')
        if action == 'Remove User':
            if user in company.company_users.all():
                company.company_users.remove(user)
                company.company_admin.remove(user)
                return Response('Removed', 200)
            else:
                return Response('Something went wrong', 201)
        elif action == 'Make Admin':
            try:
                if user not in company.company_admin.all():
                    company.company_admin.add(user)
                    return Response('Success! New admin added.', 200)
                else:
                    return Response('This user is already admin', 201)

            except Exception as e:
                print(e)
                data['result'] = str(e)
                return Response(data, 404)
        elif action == 'Remove Admin':
            if user in company.company_admin.all():
                company.company_admin.remove(user)
                return Response('Removed admin', 200)
            else:
                return Response('This admin is already removed.', 201)


class InsertInitialAddress(APIView):
    # authentication_classes = [InstallerTokenAuthentication]

    def post(self, request):
        # from pathlib import Path
        # print("File      Path:", Path(__file__).absolute())
        # print("File      Path:", Path(__file__).parent.resolve())
        # "E:/DarwinSolar/ServerProject/australia_address/australia_address.geojson"

        with open("E:/DarwinSolar/ServerProject/australia_address/australia_address.geojson", 'r') as f:
            for count, line in enumerate(f):
                # print(line)
                js = json.loads(line)
                # print(js)
                ad_hash = js['properties']['hash']
                unit = js['properties']['unit']
                number = js['properties']['number']
                street = js['properties']['street']
                city = js['properties']['city']
                district = js['properties']['district']
                region = js['properties']['region']
                postcode = js['properties']['postcode']
                address_id = js['properties']['id']
                longitude = js['geometry']['coordinates'][0]
                latitude = js['geometry']['coordinates'][1]

                # print(ad_hash)
                # print(unit)
                # print(number)
                # print(street)
                # print(city)
                # print(district)
                # print(region)
                # print(postcode)
                # print(address_id)
                # print(longitude)
                # print(latitude)
                try:
                    created = AustraliaAddressModel.objects.create(hash=ad_hash, unit=unit, number=number,
                                                                   street=street, city=city, district=district,
                                                                   state=region, postcode=postcode,
                                                                   address_original_id=address_id, longitude=longitude,
                                                                   latitude=latitude)
                    if created:
                        print(count, 'address created')
                except Exception as e:
                    print('creation error with =>', e)
                # break
        print('Total Lines', count + 1)
        return Response(f'{count} address created', 200)