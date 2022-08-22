from django.forms import model_to_dict
from rest_framework import serializers

from accounts.models import CustomUser
from company.models import Company, AddressModel, AustraliaAddressModel
from customer_portal.models import JobDetails


class CustomUserSerializer1(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'


class CompanySerializer(serializers.ModelSerializer):
    # company_user = CustomUserSerializer1(many=True)
    # company_add = serializers.SerializerMethodField()
    # billing_add = serializers.SerializerMethodField()

    class Meta:
        model = Company
        fields = ['company_name', 'company_logo', 'company_phone', 'is_active', 'company_creator']

    # def get_company_add(self, instance):
    #     # print(instance, instance.id, instance.company_address)
    #     return model_to_dict(instance.company_address)
    #
    # def get_billing_add(self, instance):
    #     # print(instance, instance.id, instance.company_name)
    #     return model_to_dict(instance.billing_address)


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddressModel
        fields = '__all__'


class AustraliaAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = AustraliaAddressModel
        fields = '__all__'


class JobDetailsSerializer1(serializers.Serializer):
    # job_panels_serials = PanelSerialNumbersSerializer(many=True, read_only=True)
    # job_number_installation_image = InstallationPhotosSerializer(many=True, read_only=True)
    # job_inverter = InverterPhotosSerializer(many=True, read_only=True)
    # customer_details = serializers.SerializerMethodField()
    #
    # def get_customer_details(self, instance):
    #     print('instance', instance.company_id)
    #     # qs = CustomUser.objects.filter(id=instance.id).values()
    #     # qs = JobDetails.objects.filter(company=instance.company_id).select_related('customer_id').values()
    #     # print('qs', qs)
    #     return qs

    class Meta:
        model = JobDetails
        fields = '__all__'

# class GroupSerializer(serializers.ModelSerializer):
#     # exp_of_group = ExpensesSerializer(many=True, read_only=True)
#     # group_final_transaction = FinalTransactionSerializer(many=True, read_only=True)
#     # group_personal_total = PersonalTotalSerializer(many=True, read_only=True)
#     calculation_cycle_group = CalculationPeriodSerializer(many=True, read_only=True)
#     # calculation_cycle = serializers.SerializerMethodField()
#
#     class Meta:
#         model = Groups
#         fields = '__all__'
#
#     def get_calculation_cycle(self, instance):
#         print('qxxxxxx', instance)
#         try:
#             qs = CalculationPeriod.objects.get(is_active=True, group_id=instance.id)
#             print('qsssssssssssssssss', qs)
#             return CalculationPeriodSerializer(qs, read_only=True).data
#         except CalculationPeriod.DoesNotExist:
#             return None
