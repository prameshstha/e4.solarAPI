from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from ds.models import DCHubDetails
from ds.api.serializer import DCHubDetailsSerializer


class DCHubDetailsList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = DCHubDetails.objects.all()
    serializer_class = DCHubDetailsSerializer


