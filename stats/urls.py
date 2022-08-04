
from django.contrib import admin
from django.urls import path

from stats.views import index, refresh, battery, batteryAjax
from . import views
app_name = 'chats_app'
urlpatterns = [
    path('', index, name='index'),
    path('battery/', battery, name='battery'),
    path('batteryAjax/', batteryAjax, name='batteryAjax'),
    path('refresh/', refresh, name='refresh'),

]
