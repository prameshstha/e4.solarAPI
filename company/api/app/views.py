from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from DarwinSolar.settings import AWS_STORAGE_BUCKET_NAME, AWS_ACCESS_KEY_ID, \
    AWS_SECRET_ACCESS_KEY, AWS_SES_REGION_NAME
import boto3
from company.api.installer_api.authentication import InstallerTokenAuthentication
from customer_portal.api.serializer import JobDetailsSerializer
from customer_portal.models import JobDetails

# ins client
client = boto3.client('s3', region_name=AWS_SES_REGION_NAME,
                      aws_access_key_id=AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
# variable
bucket = AWS_STORAGE_BUCKET_NAME


# function for deleting s3 files
def del_s3_file(filename):
    deleted = client.delete_object(Bucket=bucket, Key=filename)
    print('file deleted...')


class AllJobDetails(generics.ListCreateAPIView):
    authentication_classes = [InstallerTokenAuthentication]

    queryset = JobDetails.objects.all()
    serializer_class = JobDetailsSerializer


class SearchJobByJobNumber(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # 1267551
        job_number = self.kwargs['job_number']

        queryset = JobDetails.objects.filter(job_number=job_number)
        print(queryset, job_number)
        return queryset

    serializer_class = JobDetailsSerializer
    lookup_field = 'job_number'


