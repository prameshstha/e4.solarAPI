from rest_framework import serializers
from ds.models import DCHubDetails


class DCHubDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = DCHubDetails
        fields = '__all__'




