from django.urls import path

from ds.api.views import DCHubDetailsList


urlpatterns = [
    path('data-list/', DCHubDetailsList.as_view(), name='data-list'),

]
