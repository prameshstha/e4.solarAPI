from rest_framework import serializers
from accounts.models import CustomUser
from customer_portal.api.serializer import CustomerFilesSerializer, JobDetailsSerializer
from customer_portal.models import CustomerFiles, JobDetails, FileType, ElectricityRetailers


class AllCustomUserSerializer(serializers.ModelSerializer):
    Firstname = serializers.CharField(source='first_name')
    Lastname = serializers.CharField(source='last_name')
    CRM_Id = serializers.CharField(source='customer_crm_id')

    class Meta:
        model = CustomUser
        fields = ['id', 'Firstname', 'Lastname', 'email', 'phone', 'city', 'CRM_Id', 'street', 'postcode', 'state']


class CustomUserSerializer(serializers.ModelSerializer):
    Firstname = serializers.CharField(source='first_name')
    Lastname = serializers.CharField(source='last_name')
    CRM_Id = serializers.CharField(source='customer_crm_id')
    # customer_files = CustomerFilesSerializer(many=True, read_only=True)
    # customer_job = JobDetailsSerializer(many=True, read_only=True)
    customer_files = serializers.SerializerMethodField()
    customer_job = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['id', 'is_customer', 'Firstname', 'Lastname', 'email', 'phone', 'city', 'CRM_Id', 'street',
                  'postcode', 'state', 'customer_files', 'customer_job']

    def get_customer_files(self, instance):
        company_id = self.context.get('view').kwargs.get('company_id')
        # print('instance', instance.id, instance, 'company_id', company_id)
        qs = CustomerFiles.objects.filter(customer_id=instance.id, company=company_id).values()
        # print(qs)
        # return qs
        if qs:
            cust_files = []
            for a in qs:
                cf_id = a['file_type_id']
                f_t = FileType.objects.get(id=cf_id)
                a['file_type'] = f_t.file_type
                cust_files.append(a)
                # print(a['file_type_id'])
            # dict = model_to_dict(qs)
            return cust_files
        # return None

    def get_customer_job(self, instance):
        # print('instance cj', self.context.get('view').kwargs.get('company_id'), instance.id)
        company_id = self.context.get('view').kwargs.get('company_id')
        qs = JobDetails.objects.filter(customer_id=instance.id, company=company_id).values()
        # print(qs)
        return qs
        # if qs:
        #     cust_job = []
        #     for a in qs:
        #         cust_job.append(a)
        #     return cust_job
        # return None


class CustomUserSerializer1(serializers.ModelSerializer):
    Firstname = serializers.CharField(source='first_name')
    Lastname = serializers.CharField(source='last_name')
    CRM_Id = serializers.CharField(source='customer_crm_id')
    # customer_files = CustomerFilesSerializer(many=True, read_only=True)
    # customer_job = JobDetailsSerializer(many=True, read_only=True)
    customer_files = serializers.SerializerMethodField()
    customer_job = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['id', 'is_customer', 'Firstname', 'Lastname', 'email', 'phone', 'city', 'CRM_Id', 'street',
                  'postcode', 'state', 'customer_files', 'customer_job']

    def get_customer_files(self, instance):
        print('instance', instance.id)
        qs = CustomerFiles.objects.filter(customer_id=instance.id).values()
        # print(qs)
        if qs:
            cust_files = []
            for a in qs:
                cust_files.append(a)
            # dict = model_to_dict(qs)
            return cust_files
        return None

    def get_customer_job(self, instance):
        # print(instance.id)
        qs = JobDetails.objects.filter(customer_id=instance.id).values()
        if qs:
            cust_job = []
            for a in qs:
                cust_job.append(a)
            return cust_job
        return None


class RegistrationSerializer(serializers.ModelSerializer):
    # password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = CustomUser
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def save(self):
        password = self.validated_data['password']
        account = CustomUser(email=self.validated_data['email'], first_name=self.validated_data['first_name'],
                             last_name=self.validated_data['last_name'],
                             customer_crm_id=self.validated_data['customer_crm_id'],
                             street=self.validated_data['street'], city=self.validated_data['city'],
                             postcode=self.validated_data['postcode'],
                             state=self.validated_data['state'], country=self.validated_data['country'],
                             phone=self.validated_data['phone'])

        # account = User(email=self.validated_data['email'],
        account.set_password(password)
        account.save()
        return account


class ChangePasswordSerializer(serializers.Serializer):
    model = CustomUser

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class ElectricityRetailersSerializer(serializers.ModelSerializer):

    class Meta:
        model = ElectricityRetailers
        fields = '__all__'
