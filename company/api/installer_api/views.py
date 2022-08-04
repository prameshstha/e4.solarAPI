import os

from django.contrib.auth import logout
from django.contrib.auth.hashers import check_password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import EmailMultiAlternatives
from django.forms import model_to_dict
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
import requests as apiRequest
from DarwinSolar.utils import EmailThread, get_filename_ext
from accounts.api.serializer import AllCustomUserSerializer, CustomUserSerializer
from company.api.app.views import del_s3_file
from company.api.company_api.serializer import CompanySerializer
from company.api.installer_api.authentication import InstallerTokenAuthentication
from company.api.installer_api.serializer import InstallerUserSerializer, RegistrationInstallerUserSerializer, \
    ChangePasswordSerializer, InstallerEmailSerializer, ResetPasswordSerializer
from accounts.models import InstallerUser, InstallerToken, CustomUser
from company.models import Company
from customer_portal.api.serializer import CustomerFilesSerializer, JobDetailsSerializer, CommonCustomerFileSerializer
from customer_portal.models import CustomerFiles, FileType, JobDetails, CommonCustomerFile

from DarwinSolar.settings import AWS_S3_CUSTOM_DOMAIN, AWS_STORAGE_BUCKET_NAME, AWS_ACCESS_KEY_ID, \
    AWS_SECRET_ACCESS_KEY, AWS_SES_REGION_NAME
import boto3

# ins client
client = boto3.client('s3', region_name=AWS_SES_REGION_NAME,
                      aws_access_key_id=AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
# variable
bucket = AWS_STORAGE_BUCKET_NAME


class CustomerListView(generics.ListCreateAPIView):
    authentication_classes = [InstallerTokenAuthentication]
    queryset = CustomUser.objects.all()
    serializer_class = AllCustomUserSerializer


class CustomerEditDeleteView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [InstallerTokenAuthentication]  # for custom authentication for Installer User table

    def get_queryset(self):
        print(self.kwargs)
        customer_id = self.kwargs['pk']

        queryset = CustomUser.objects.filter(id=customer_id)
        return queryset

    serializer_class = CustomUserSerializer


class InstallerListView(generics.ListCreateAPIView):
    authentication_classes = [InstallerTokenAuthentication]  # for custom authentication for Installer User table
    queryset = InstallerUser.objects.all()
    serializer_class = InstallerUserSerializer


class InstallerEditDeleteView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [InstallerTokenAuthentication]  # for custom authentication for Installer User table
    queryset = InstallerUser.objects.all()
    serializer_class = InstallerUserSerializer


class AllCustomerFileView(generics.ListCreateAPIView):
    authentication_classes = [InstallerTokenAuthentication]  # for custom authentication for Installer User table
    queryset = CustomerFiles.objects.all()
    serializer_class = CustomerFilesSerializer


class CustomerFileView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [InstallerTokenAuthentication]  # for custom authentication for Installer User table
    queryset = CustomerFiles.objects.all()
    serializer_class = CustomerFilesSerializer
    lookup_field = 'customer_id'


class AllFileTypeView(APIView):
    authentication_classes = [InstallerTokenAuthentication]  # for custom authentication for Installer User table

    def get(self, request, **kwargs):
        company = self.kwargs['company']
        queryset = FileType.objects.filter(company=company).values()
        return Response(queryset, 200)

    def post(self, request, **kwargs):
        print('filetye create', request.data, kwargs)
        # file_id = request.data['id']
        file_type = request.data['file_type']
        file_details = request.data['file_details']
        company_id = self.kwargs['company']
        to_email = request.data['to_email']
        company = Company.objects.get(id=company_id)
        file_type_already = FileType.objects.filter(file_type=file_type, company=company_id)
        print('already', file_type_already)

        # print(queryset)
        if file_type_already:
            return Response('File type already exists', 409)
        else:
            queryset = FileType.objects.create(file_type=file_type, file_details=file_details, company=company,
                                               to_email=to_email)
            if queryset:
                return Response('success', 201)
            else:
                print(queryset)
                return Response('failed', 400)

    def patch(self, request, **kwargs):
        print('filetye edit', request.data, kwargs)
        company = self.kwargs['company']
        file_id = request.data['id']
        file_type = request.data['file_type']
        file_details = request.data['file_details']
        to_email = request.data['to_email']
        old_file_name = FileType.objects.get(company=company, id=file_id)
        old_file_name.file_type = file_type
        old_file_name.file_details = file_details
        old_file_name.to_email = to_email
        old_file_name.save()
        print(old_file_name)
        return Response('success', 200)

    def delete(self, request, **kwargs):
        print('filetye delete', request.data, kwargs)
        file_id = self.kwargs['company']
        queryset = FileType.objects.get(id=file_id).delete()
        print(queryset)
        return Response(queryset, 204)

    # serializer_class = FileTypeSerializer


# for customer view
class CommonCustomerFileView(APIView):
    # permission_classes = [IsAuthenticated]
    def post(self, request, **kwargs):
        print(kwargs, request.data)
        company_id = kwargs['company']
        if request.data:
            company = Company.objects.get(id=company_id)
            panel = request.data.get('panel').split()[0]
            print(panel)
            inverter = request.data.get('inverter').split()[0]
            print(inverter)
            hotwater = request.data.get('hotwater', 'none')
            aircon = request.data.get('aircon', 'none')
            pan = CommonCustomerFile.objects.filter(file_name__icontains=panel, company=company)
            inv = CommonCustomerFile.objects.filter(file_name__icontains=inverter, company=company)
            hw = CommonCustomerFile.objects.filter(file_name__icontains=hotwater, company=company)
            ac = CommonCustomerFile.objects.filter(file_name__icontains=aircon, company=company)
            f_pan, f_inv, f_hw, f_ac = '', '', '', ''
            dict = {}
            print(pan, inv, hw, ac)
            if pan:
                f_pan = pan.values('file').first()
            if inv:
                f_inv = inv.values('file').first()
            if hw:
                f_hw = hw.values('file').first()
            if ac:
                f_ac = ac.values('file').first()
            dict['solar_panel'] = f_pan['file'] if f_pan else ''
            dict['inverter'] = f_inv['file'] if f_inv else ''
            dict['hotwater'] = f_hw['file'] if f_hw else ''
            dict['aircon'] = f_ac['file']if f_ac else ''
            return Response(dict, 200)
        return Response('Not now', 200)

    # def get_queryset(self):
    #     company_id = self.kwargs['company']
    #     print(self.kwargs, self.request.data)
    #     queryset = CommonCustomerFile.objects.filter(company=company_id)
    #     return queryset
    # serializer_class = CommonCustomerFileSerializer


class CommonFileView(APIView):
    authentication_classes = [InstallerTokenAuthentication]  # for custom authentication for Installer User table

    def get(self, request, **kwargs):
        company = self.kwargs['company']
        queryset = CommonCustomerFile.objects.filter(company=company).values()
        return Response(queryset, 200)

    def post(self, request, **kwargs):
        print('common file create', request.data, kwargs)
        data = {}
        print('file serializer', request.data)
        f_name = request.data.get('file_name', '')
        # file = request.data.get('file', '')
        # f_details = request.data.get('file_details', '')
        model_number = request.data.get('model_number', '')
        company_id = kwargs['company']
        name, ext = os.path.splitext(f_name)

        company = Company.objects.get(id=company_id)
        print(company_id, company)
        # print(file_type, 'job', job.customer_id.first_name)
        # request.data.update(file_type=file_type)
        # request.data.update(company=company)
        try:
            file_already = CommonCustomerFile.objects.get(file_name=f_name, company=company, model_number=model_number)
            print(file_already.file)
            file_already.delete()
            # CustomerFiles.file.delete(save=False)
            try:
                del_s3_file(str(file_already.file))
            except Exception as er:
                print(er)
        except CommonCustomerFile.DoesNotExist:
            print('No file found')
        # job_numb = request.data['job_numb']
        fileSerializer = CommonCustomerFileSerializer(data=request.data)
        print(fileSerializer.is_valid())
        print(fileSerializer.errors)
        if fileSerializer.is_valid():
            print('uploaded common file')
            uploaded_file = fileSerializer.save()

            if uploaded_file:
                print('file uploaded', uploaded_file.file)
                # uploaded_file.job_number = job
                # uploaded_file.file_type = file_type
                uploaded_file.file_name = name
                uploaded_file.save()
                data['filePath'] = str(uploaded_file.file)
                data['uploadedFileName'] = str(uploaded_file.file_name)
                data['success'] = 'success'
                # start send email to respective parties
                # file_path = data["filePath"]
                full_file_path = f'https://{AWS_S3_CUSTOM_DOMAIN}/{data["filePath"]}'
                data['full_file_path'] = full_file_path
                print('full_file_path')
                # if file_type == 'COC' or 'Power and Water':
                #     send_email_about_files(full_file_path, file_type.file_type, customer_id, f_name, job, ext)
                # end send email to respective parties

                return Response(data, 200)
        else:
            fileSerializer.errors['status'] = False
            data['error'] = fileSerializer.errors
            return Response(data, 409)

    def patch(self, request, **kwargs):
        print('common file edit', request.data, kwargs)
        company = self.kwargs['company']
        file_id = request.data['id']
        file_name = request.data['file_name']
        file_details = request.data['file_details']
        model_number = request.data['model_number']
        file = request.data['file']
        has_file = request.data.get('hasFile', '')
        print('has file', file, has_file, 'hasss fileeee')
        if has_file:
            try:
                file_already = CommonCustomerFile.objects.get(id=file_id, company=company)
                print(file_already.file)
                try:
                    del_s3_file(str(file_already.file))
                except Exception as er:
                    print(er)
                fileSerializer = CommonCustomerFileSerializer(file_already, data=request.data, partial=True)
                print(fileSerializer.is_valid())
                print(fileSerializer.errors)
                if fileSerializer.is_valid():
                    # self.perform_update()
                    fileSerializer.save()
                return Response('Edited', 200)
            except CommonCustomerFile.DoesNotExist:
                print('No file found')
                return Response('Not Edited', 401)
            # job_numb = request.data['job_numb']

        else:
            try:
                old_file_name = CommonCustomerFile.objects.get(company=company, id=file_id)
                old_file_name.file_name = file_name
                old_file_name.file_details = file_details
                old_file_name.model_number = model_number
                old_file_name.save()
                print(old_file_name)
            except CommonCustomerFile.DoesNotExist:
                return Response('Please refresh and try again', 400)
            return Response('success', 200)

    def delete(self, request, **kwargs):
        print('common file delete', request.data, kwargs)
        file_id = self.kwargs['company']
        try:
            file_already = CommonCustomerFile.objects.get(id=file_id)
            print(file_already.file)
            # CustomerFiles.file.delete(save=False)
            try:
                del_s3_file(str(file_already.file))
            except Exception as er:
                print(er)
            file_already.delete()
        except CommonCustomerFile.DoesNotExist:
            print('No file found')
        return Response('Deleted', 204)


class CustomerJob(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [InstallerTokenAuthentication]  # for custom authentication for Installer User table
    queryset = JobDetails.objects.all()
    serializer_class = JobDetailsSerializer
    lookup_field = 'customer_id'


def modify_input_for_multiple_files(customer_id, job_number, image_list):
    customer_file = {'customer_id': customer_id, 'file': image_list, "job_number": job_number}
    return customer_file


class AddCustomerFiles(APIView):
    authentication_classes = [InstallerTokenAuthentication]  # for custom authentication for Installer User table

    def post(self, request):
        data = {}
        print('file serializer', request.data)
        f_type = request.data['file_typ']
        f_name = request.data['name']
        name, ext = os.path.splitext(f_name)
        customer_id = request.data['customer_id']
        company_id = request.data['company']
        job = JobDetails.objects.get(customer_id=customer_id)
        company = Company.objects.get(id=company_id)
        print(company_id, company)
        file_type = FileType.objects.get(file_type=f_type)
        # print(file_type, 'job', job.customer_id.first_name)
        request.data.update(file_type=file_type)
        # request.data.update(company=company)
        try:
            file_type_already = CustomerFiles.objects.get(file_type=file_type, customer_id=customer_id, job_number=job)
            print(file_type_already.file)
            file_type_already.delete()
            # CustomerFiles.file.delete(save=False)
            try:
                del_s3_file(str(file_type_already.file))
            except Exception as er:
                print(er)
        except CustomerFiles.DoesNotExist:
            print('No file found')
        # job_numb = request.data['job_numb']
        fileSerializer = CustomerFilesSerializer(data=request.data)
        # print(fileSerializer.is_valid())
        # print(fileSerializer.errors)
        if fileSerializer.is_valid():
            print('uploaded file')
            uploaded_file = fileSerializer.save()

            if uploaded_file:
                print('file uploaded', uploaded_file.file)
                # uploaded_file.job_number = job
                uploaded_file.file_type = file_type
                uploaded_file.file_name = name
                uploaded_file.save()
                data['filePath'] = str(uploaded_file.file)
                data['uploadedFileName'] = str(uploaded_file.file_name)
                data['success'] = 'success'
                # start send email to respective parties
                # file_path = data["filePath"]
                full_file_path = f'https://{AWS_S3_CUSTOM_DOMAIN}/{data["filePath"]}'
                data['full_file_path'] = full_file_path
                print('uploaded file email', file_type.to_email)
                if file_type.to_email:
                    send_email_about_files(file_type.to_email, full_file_path, file_type.file_type, customer_id, f_name,
                                           job, ext)
                # if file_type == 'COC' or 'Power and Water':
                #     send_email_about_files(full_file_path, file_type.file_type, customer_id, f_name, job, ext)
                # end send email to respective parties

                return Response(data, 200)
        else:
            fileSerializer.errors['status'] = False
            data['error'] = fileSerializer.errors
            return Response(data, 409)


class PvApplicationView(APIView):
    authentication_classes = [InstallerTokenAuthentication]

    def post(self, request, **kwargs):
        print(request.data, kwargs)
        # a = request.data['a']
        files = request.data.get('selectedFiles')
        commonfiles = request.data.get('selectedCommonFiles')
        company_id = kwargs['company_id']
        customer_id = request.data.get('customer_id')
        customer = CustomUser.objects.get(id=customer_id)
        company = Company.objects.get(id=company_id)
        job = JobDetails.objects.get(customer_id=customer_id)
        email_files = []
        list_file = {}
        for i in files:
            list_file['customer_file'] = CustomerFiles.objects.get(file_type=i, company=company_id, customer_id=customer_id)
            list_file['file_type'] = FileType.objects.get(id=i, company=company_id)
            email_files.append(list_file.copy())
        email_common_files = []
        list_files = {}
        for j in commonfiles:
            list_files['common_file'] = CommonCustomerFile.objects.get(id=j, company=company_id)
            email_common_files.append(list_files.copy())

        pv_application_email(email_files, email_common_files, customer, company, job)
        # print('outside loop', email_common_files)
        return Response('test ', 200)


def pv_application_email(email_file, email_common_files, customer, company, job):
    # print(email_file, customer, company)
    media_url = f'https://{AWS_S3_CUSTOM_DOMAIN}/'
    merge_data = {
        'company': 'test Customer',
        'customer_email': 'customer email',
        'job': job,}
    to_email = []
    for a in email_file:
        # print(media_url+str(a['customer_file'].file))
        to_email.append(a['file_type'].to_email)

    # full_file_path = f'https://{AWS_S3_CUSTOM_DOMAIN}/{customer_file.file}'
    # print(to_email)
    try:
        email_subject = f"PV Application of {job.customer_id.first_name} {job.customer_id.last_name}"
        email_html_body = render_to_string("send_pv_application.html", merge_data)
        from_email = "utilities@darwinsolar.com.au"  # change form email according to company settings 29/07/2022
        # to_email = [to_email]
        send_email = EmailMultiAlternatives(
            email_subject,
            email_html_body,
            from_email,
            to_email,
            # ['reception@darwinsolar.com.au']
        )
        # download = apiRequest.get(full_file_path)
        # LineDiagram = apiRequest.get('https://darwinsolar-bucket.s3.amazonaws.com/Files/LineDiagram.pdf')
        # cc = apiRequest.get('https://darwinsolar-bucket.s3.amazonaws.com/Files/cc.png')

        # send_email.attach(customer_file.file_name, download.content)  # attach file form s3
        # send_email.attach('LineDiagram.pdf', LineDiagram.content)  # attach file form s3
        # send_email.attach('cc.png', cc.content)  # attach file form s3

        for a in email_file:
            # print(media_url+str(a['customer_file'].file))
            file_s3_aws = apiRequest.get(media_url + str(a['customer_file'].file))
            # print(get_filename_ext(str(a['customer_file'].file)))
            file_name, ext = get_filename_ext(str(a['customer_file'].file))
            send_email.attach(a['customer_file'].file_name + ext, file_s3_aws.content)

        for b in email_common_files:
            # print(media_url + str(b['common_file'].file))
            print(b['common_file'].file_name)
            file_s3_aws = apiRequest.get(media_url + str(b['common_file'].file))
            # print(get_filename_ext(str(b['common_file'].file)))
            file_name, ext = get_filename_ext(str(b['common_file'].file))
            send_email.attach(b['common_file'].file_name+ext, file_s3_aws.content)

        send_email.attach_alternative(email_html_body, "text/html")
        EmailThread(send_email).start()  # to send email faster
    except Exception as e:
        print(e)
    pass


def send_email_about_files(to_email, path, file_type, customer_id, file_name, job, ext):
    #  temporary solution for sending email for beta testing for Darwin Solar. 07/07/2022
    print(to_email, path, file_type, customer_id)
    merge_data = {
        'file_type': file_type,
        'to_email': to_email,
        'job': job,
    }
    try:
        email_subject = f"{file_type} file of {job.customer_id.first_name} {job.customer_id.last_name}"
        email_html_body = render_to_string(
            "email_attached_file.html", merge_data)
        from_email = "utilities@darwinsolar.com.au"  # change form email according to company settings 07/07/2022
        to_email = [to_email]
        send_email = EmailMultiAlternatives(
            email_subject,
            email_html_body,
            from_email,
            to_email,
            # ['reception@darwinsolar.com.au']
        )
        download = apiRequest.get(path)
        # file_name, ext = get_filename_ext(str(a['customer_file'].file))
        print()
        send_email.attach(file_name, download.content)  # attach file form s3
        send_email.attach_alternative(email_html_body, "text/html")
        EmailThread(send_email).start()  # to send email faster
    except Exception as e:
        print(e)


# def check_file_type_to_send_email(file_type):
#     print(file_type, type(file_type), file_type == 'Power and Water')
#     if file_type == 'Power and Water':
#         # email to power and water nt connect.me@powerwater.com.au; CONNECT.ME@qms.powerwater.com.au
#         return 'pramesh@darwinsolar.com.au'
#     elif file_type == 'COC':
#         # coc sent to power and water?? powerconnections@powerwater.com.au; PowerConnections.PWC@powerwater.com.au
#         # connect.me@powerwater.com.au
#         # PowerConnections.PWC@powerwater.com.au
#         return 'admin@darwinsolar.com.au'


class Login(APIView):
    def post(self, request):
        # serializer = LoginSerializer(data=request.data)
        print(request.data)
        email = request.data['email']
        print(email)
        password = request.data['password']

        if email and password:
            try:
                # Try to find a user matching your username
                user = InstallerUser.objects.get(email=email)
                pwd_valid = check_password(password, user.password)
                # print(pwd_valid)
                #  Check the password is the reverse of the username
                # something wrong here need to check asap
                if pwd_valid:
                    # Yes? return the Django user object
                    token = InstallerToken.objects.get_or_create(user=user)

                    # change according to the needs
                    # if users are installer or admin of multiple company
                    # company = Company.objects.filter(company_users=user)

                    # if users are installer or admin single company
                    company = Company.objects.filter(company_users=user)
                    all_company = Company.objects.filter(company_users=user).values()
                    # print('company', company, 'all company', all_company)
                    user_dict = (model_to_dict(user))
                    user_dict.pop('last_login')
                    user_dict.pop('date_joined')
                    user_dict.pop('password')
                    # print(token[0])
                    user_dict['token'] = str(token[0])
                    # user_dict['company_id'] = company.id
                    # user_dict['company_name'] = company.company_name
                    user_dict['company'] = all_company  # if user are installer of multiple company
                    # user_dict['company_name'] = company.company_name
                    admin = []
                    for a in company:
                        if user in a.company_admin.all():
                            admin.append(a.company_name)
                        user_dict['admin'] = admin
                    print('list admin', admin)

                    # if user in company.company_admin.all():
                    #     print('turee')
                    #
                    #     user_dict['is_admin'] = True

                    # print(user_dict)

                    # jobs_open = JobDetails.objects.filter(company=company, is_open=True)
                    # print(jobs_open)
                    # k = json.loads(serialize('json', jobs_open))
                    # print('kkkk', k)

                    # # start To change the job company id manually
                    # company = Company.objects.filter(company_users=user).first()
                    # print(company)
                    # # print(i.company_admin, 'admin')
                    # # print(i.company_users.all())
                    # for a in company.company_customers.all():
                    #     print(a.email)
                    #     user = CustomUser.objects.get(email=a.email)
                    #     print('user here', user)
                    #     jobd = JobDetails.objects.get(customer_id=user)
                    #     print(jobd.company)
                    #     jobd.company = company
                    #     jobd.save()
                    #     print(jobd.company)
                    # # end To change the job company id manually

                    # user_dict['jobs_open'] = k

                    return Response(user_dict, 200)
                else:
                    # No? return None - triggers default login failed
                    return Response({'Error': 'Email or Password wrong'}, 403)
            except InstallerUser.DoesNotExist:
                # No user was found, return None - triggers default login failed
                return Response({'Error': 'User Does not exist'}, 404)
        else:
            Response('Not Logged in', 401)


#
# class AllCompanyJobDetails(generics.ListCreateAPIView):
#     authentication_classes = [InstallerTokenAuthentication]
#
#     queryset = JobDetails.objects.all()
#     serializer_class = JobDetailsSerializer
#     lookup_field = 'company'


# class RegistrationView(APIView):
#     # permission_classes = [IsAuthenticated]
#
#     def post(self, request):
#         print(request.data)
#
#         account_serializer = RegistrationInstallerUserSerializer(data=request.data)
#         # print(account_serializer.is_valid(), job_details_serializer.is_valid(), customer_files_serializer.is_valid())
#
#         data = {}
#         if account_serializer.is_valid():
#             print('valid')
#             user = account_serializer.save()
#             token = InstallerToken.objects.create(user=user)
#
#             print(user)
#             # email user with email and password
#             # ask user to change password
#
#             link = "darwin.solar"
#             # print(sender, "sender", instance, "instance", reset_password_token, "reset_password_token",
#             #       reset_password_token.user.email)
#             print(link)
#             print(user.first_name, user.email)
#             customer = user.first_name
#             if user.first_name == '':
#                 customer = user.email
#             merge_data = {
#                 'customer': customer,
#                 'customer_email': user.email,
#                 'link': link,  # change in production level
#                 'password': 'darwinsolar@2022'
#             }
#
#             email_subject = "Welcome to Darwin Solar portal."
#             email_html_body = render_to_string("welcome.html", merge_data)
#             from_email = "reception@darwinsolar.com.au"
#             to_email = [user.email]
#             send_email = EmailMultiAlternatives(
#                 email_subject,
#                 email_html_body,
#                 from_email,
#                 to_email,
#
#             )
#             send_email.attach_alternative(email_html_body, "text/html")
#             EmailThread(send_email).start()  # to send email faster
#
#             data = {'User created'}
#
#             return Response(data, 200)
#         else:
#             data = account_serializer.errors
#             print(data)
#         return Response(data, 403)


class Logout(APIView):
    authentication_classes = [InstallerTokenAuthentication]  # for custom authentication for Installer User table

    def post(self, request):
        print(request.user)
        print(request.data)
        logout(request)
        return Response({'message': 'User Logged out'})


class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    authentication_classes = [InstallerTokenAuthentication]  # for custom authentication for Installer User table
    serializer_class = ChangePasswordSerializer
    model = InstallerUser

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


class InstallerPasswordReset(generics.UpdateAPIView):
    """
        Request for Password Reset Link.
        """

    serializer_class = InstallerEmailSerializer

    def post(self, request):
        """
        Create token.
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data["email"]
        user = InstallerUser.objects.filter(email=email).first()
        if user:
            encoded_pk = urlsafe_base64_encode(force_bytes(user.pk))
            token = PasswordResetTokenGenerator().make_token(user)
            link = "{}?resetid={}&token={}".format('password-reset-inst', encoded_pk, token)

            # send the rest_link as mail to the user.
            user = InstallerUser.objects.get(email=user.email)
            print(user.first_name, user.email)
            customer = user.first_name
            if user.first_name == '':
                customer = user.email
            print(customer)
            pw_reset_link = 'http://localhost:3000/' + link
            # pw_reset_link = 'e4.solar' + link  # change in production level
            merge_data = {
                'customer': customer,
                'pw_reset_link': pw_reset_link  # change in production level
            }
            email_subject = "Password Reset for {title}".format(title="Darwin Solar Portal")
            email_html_body = render_to_string("reset_password_email.html", merge_data)
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

            return Response(
                {
                    "message":
                        f"Your password rest link: {pw_reset_link}",
                    "encoded_pk": encoded_pk, "token": token
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"message": "User doesn't exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ResetPasswordAPI(generics.GenericAPIView):
    """
    Verify and Reset Password Token View.
    """
    serializer_class = ResetPasswordSerializer

    def post(self, request, *args, **kwargs):
        """
        Verify token & encoded_pk and then reset the password.
        """
        print('rpa', request.data)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            {"message": "Password reset complete"},
            status=status.HTTP_200_OK,
        )
