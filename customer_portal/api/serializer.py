from rest_framework import serializers
from accounts.models import CustomUser
from company.models import Company
from customer_portal.models import CustomerFiles, JobDetails, FileType, PanelSerialNumbers, InstallationPhotos, \
    InverterPhotos, CommonCustomerFile


class FileTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = FileType
        fields = '__all__'


class CustomerFilesSerializer(serializers.ModelSerializer):
    file_type = serializers.StringRelatedField()
    # job_number = serializers.StringRelatedField()
    #
    job_number = serializers.SlugRelatedField(
        # many=True,
        queryset=JobDetails.objects.all(),
        slug_field='job_number'
    )
    company = serializers.SlugRelatedField(
        # many=True,
        queryset=Company.objects.all(),
        slug_field='id'
    )

    class Meta:
        model = CustomerFiles
        fields = '__all__'


class InstallationPhotosSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstallationPhotos
        fields = '__all__'


class InverterPhotosSerializer(serializers.ModelSerializer):
    class Meta:
        model = InverterPhotos
        fields = '__all__'


class PanelSerialNumbersSerializer(serializers.ModelSerializer):
    class Meta:
        model = PanelSerialNumbers
        fields = '__all__'


class CustomUserSerializer1(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = '__all__'


class CommonCustomerFileSerializer(serializers.ModelSerializer):

    class Meta:
        model = CommonCustomerFile
        fields = '__all__'

    def patch(self, instance, validated_data):
        print(instance, 'validated', validated_data)


class JobDetailsSerializer(serializers.ModelSerializer):
    job_panels_serials = PanelSerialNumbersSerializer(many=True, read_only=True)
    job_number_installation_image = InstallationPhotosSerializer(many=True, read_only=True)
    job_inverter = InverterPhotosSerializer(many=True, read_only=True)

    class Meta:
        model = JobDetails
        fields = '__all__'


    # def update(self, instance, validated_data):
    #     print('validated data for update', validated_data)
    #     for attr, value in validated_data.items():
    #         print('all data', instance, attr, value)
    #         setattr(instance, attr, value)
    #     instance.save()
    #     return instance

