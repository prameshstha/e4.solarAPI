import requests as apiRequest
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from DarwinSolar.settings import AWS_STORAGE_BUCKET_NAME, AWS_ACCESS_KEY_ID, \
    AWS_SECRET_ACCESS_KEY, AWS_SES_REGION_NAME
import boto3

from accounts.api.serializer import CustomUserSerializer

from DarwinSolar.utils import EmailThread
from accounts.models import CustomUser, InstallerUser
from company.api.installer_api.authentication import InstallerTokenAuthentication
from customer_portal.api.serializer import CustomerFilesSerializer, JobDetailsSerializer, FileTypeSerializer

from company.models import Company
from customer_portal.models import CustomerFiles, JobDetails, FileType

# ins client
client = boto3.client('s3', region_name=AWS_SES_REGION_NAME,
                      aws_access_key_id=AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
# variable
bucket = AWS_STORAGE_BUCKET_NAME


# # list all objs in bucket
# all_objects = client.list_objects(Bucket=bucket)
# # print the contents
# print(f'List of object in {bucket}:')
# for a in all_objects['Contents']:
#     print(a['Key'])


# function for deleting s3 files
def del_s3_file(filename):
    deleted = client.delete_object(Bucket=bucket, Key=filename)
    print('file deleted...')


class AllCustomerFileView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = CustomerFiles.objects.all()
    serializer_class = CustomerFilesSerializer


class CustomerFileView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = CustomerFiles.objects.all()
    serializer_class = CustomerFilesSerializer
    lookup_field = 'customer_id'


class AllFileTypeView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        company_id = self.kwargs['company_id']
        queryset = FileType.objects.filter(company=company_id)
        return queryset
    serializer_class = FileTypeSerializer


class EditDeleteFileTypeView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = FileType.objects.all()
    serializer_class = FileTypeSerializer


class CustomerJob(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = JobDetails.objects.all()
    serializer_class = JobDetailsSerializer
    lookup_field = 'customer_id'


class CustomerJobEditByUser(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [InstallerTokenAuthentication]
    queryset = JobDetails.objects.all()
    serializer_class = JobDetailsSerializer
    lookup_field = 'customer_id'


def send_email_to_user(company_id, job, customer, user):
    company = Company.objects.get(id=company_id)
    merge_data = {
        'user': user,
        'job': job,
        'customer': customer,
        'company': company
    }
    # print(company.company_users.all().values_list('email', flat=True))
    user_email_list = list(company.company_users.all().values_list('email',flat=True))
    try:
        email_subject = f"{job.job_number} of {job.customer_id.first_name} {job.customer_id.last_name}"
        email_html_body = render_to_string(
            "customer_data_saved.html", merge_data)
        from_email = user.email  # change form email according to company settings 16/08/2022
        send_email = EmailMultiAlternatives(
            email_subject,
            email_html_body,
            from_email,
            user_email_list,
            # ['reception@darwinsolar.com.au']
        )
        send_email.attach_alternative(email_html_body, "text/html")
        EmailThread(send_email).start()  # to send email faster
    except Exception as e:
        print(e)
    pass


class EditCustomerAllDetails(APIView):
    authentication_classes = [InstallerTokenAuthentication]

    def patch(self, request, **kwargs):
        # print(request.data, kwargs)
        is_finalized = kwargs.get('is_finalized')
        # print('finalize', is_finalized,  eval(is_finalized))
        user_id = request.data.get('user')
        user = InstallerUser.objects.get(id=user_id)
        job = JobDetails.objects.get(job_number=request.data.get('job_number'))
        customer = CustomUser.objects.get(id=request.data.get('customer_id'))
        job_serializer = JobDetailsSerializer(job, data=request.data, partial=True)
        customer_serializer = CustomUserSerializer(customer, data=request.data, partial=True)
        # print(job_serializer.is_valid(), customer_serializer.is_valid())
        # print(job_serializer.errors, customer_serializer.errors)
        if job_serializer.is_valid():
            job = job_serializer.save()
            if eval(is_finalized):
                # print('final')
                job.finalized_by = user
                job.save()
                # if save send notification to reception
                send_email_to_user(request.data.get('company'), job, customer, user)
            if customer_serializer.is_valid():
                customer_serializer.save()


        return Response('tested', 200)


def modify_input_for_multiple_files(customer_id, job_number, image_list):
    customer_file = {'customer_id': customer_id, 'file': image_list, "job_number": job_number}
    return customer_file


# class AddCustomerFiles(APIView):
#     permission_classes = [IsAuthenticated]
#     authentication_classes = [InstallerTokenAuthentication]  # for custom authentication for Installer User table
#
#     def post(self, request):
#         data = {}
#         print('file serializer', request.data)
#         f_type = request.data['file_typ']
#         f_name = request.data['name']
#         name, ext = os.path.splitext(f_name)
#         customer_id = request.data['customer_id']
#         job = JobDetails.objects.get(customer_id=customer_id)
#         file_type = FileType.objects.get(file_type=f_type)
#         # print(file_type, 'job', job.customer_id.first_name)
#         request.data.update(file_type=file_type)
#         try:
#             file_type_already = CustomerFiles.objects.get(file_type=file_type, customer_id=customer_id, job_number=job)
#             print(file_type_already.file)
#             file_type_already.delete()
#             # CustomerFiles.file.delete(save=False)
#             try:
#                 del_s3_file(str(file_type_already.file))
#             except Exception as er:
#                 print(er)
#         except CustomerFiles.DoesNotExist:
#             print('No file found')
#         # job_numb = request.data['job_numb']
#         fileSerializer = CustomerFilesSerializer(data=request.data)
#         print(fileSerializer.is_valid(), fileSerializer)
#         # print(fileSerializer.errors)
#         if fileSerializer.is_valid():
#             print('uploaded file', fileSerializer)
#             uploaded_file = fileSerializer.save()
#
#             if uploaded_file:
#                 print('file uploaded', uploaded_file.file)
#                 # uploaded_file.job_number = job
#                 uploaded_file.file_type = file_type
#                 uploaded_file.file_name = name
#                 uploaded_file.save()
#                 data['filePath'] = str(uploaded_file.file)
#                 data['uploadedFileName'] = str(uploaded_file.file_name)
#                 data['success'] = 'success'
#                 # start send email to respective parties
#                 # file_path = data["filePath"]
#                 full_file_path = f'https://{AWS_S3_CUSTOM_DOMAIN}/{data["filePath"]}'
#                 if file_type == 'COC' or 'Power and Water':
#                     send_email_about_files(full_file_path, file_type.file_type, customer_id, f_name, job, ext)
#                 # end send email to respective parties
#
#                 return Response(data, 200)
#         else:
#             fileSerializer.errors['status'] = False
#             data['error'] = fileSerializer.errors
#         return Response(data, 409)


class SearchJob(generics.ListAPIView):

    def get_queryset(self):
        # 1267551
        customer_hs_id = self.kwargs['customer_hs_id']

        queryset = JobDetails.objects.filter(customer_hs_id=customer_hs_id)
        return queryset

    serializer_class = JobDetailsSerializer
    lookup_field = 'customer_hs_id'


def send_email_about_files(path, file_type, customer_id, file_name, job, ext):
    # print(path, file_type, customer_id)
    merge_data = {
        'customer': 'test Customer',
        'customer_email': 'customer email',
        'job': job,
    }
    try:
        email_subject = "File for this customer"
        email_html_body = render_to_string("send_coc_attachment.html" if file_type == 'COC' else "send_pv_application.html", merge_data)
        from_email = "utilities@darwinsolar.com.au"
        toemail = check_file_type_to_send_email(file_type)
        to_email = [toemail]
        send_email = EmailMultiAlternatives(
            email_subject,
            email_html_body,
            from_email,
            to_email,
            # ['reception@darwinsolar.com.au']
        )
        download = apiRequest.get(path)
        LineDiagram = apiRequest.get('https://darwinsolar-bucket.s3.amazonaws.com/Files/LineDiagram.pdf')
        cc = apiRequest.get('https://darwinsolar-bucket.s3.amazonaws.com/Files/cc.png')

        send_email.attach(file_name, download.content)  # attach file form s3
        if file_type == 'Power and Water':
            send_email.attach('LineDiagram.pdf', LineDiagram.content)  # attach file form s3
            send_email.attach('cc.png', cc.content)  # attach file form s3
        send_email.attach_alternative(email_html_body, "text/html")
        # EmailThread(send_email).start()  # to send email faster
    except Exception as e:
        print(e)


def check_file_type_to_send_email(file_type):
    # print(file_type, type(file_type), file_type == 'Power and Water')
    if file_type == 'Power and Water':
        # email to power and water nt connect.me@powerwater.com.au; CONNECT.ME@qms.powerwater.com.au
        return 'pramesh@darwinsolar.com.au'
    elif file_type == 'COC':
        # coc sent to power and water?? powerconnections@powerwater.com.au; PowerConnections.PWC@powerwater.com.au
        # connect.me@powerwater.com.au
        # PowerConnections.PWC@powerwater.com.au
        return 'admin@darwinsolar.com.au'


class ZapTest(APIView):
    def post(self, request):
        print(request.data)
        pass
