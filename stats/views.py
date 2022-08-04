import datetime as datetime

import pytz
import requests
from dateutil.tz import tzlocal
from django.contrib.auth.models import User
from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from ds.models import DCHubDetails
from django.shortcuts import HttpResponse
from datetime import timezone
from dateutil.parser import parse

# Create your views here.
baseUrl = 'http://127.0.0.1:8000/'
dataList = 'ds/data-list/'
unique_time = ['00:00', '00:05', '00:10', '00:15', '00:20', '00:25', '00:30', '00:35', '00:40', '00:45', '00:50',
               '00:55', '01:00', '01:05', '01:10', '01:15', '01:20', '01:25', '01:30', '01:35', '01:40', '01:45',
               '01:50', '01:55', '02:00', '02:05', '02:10', '02:15', '02:20', '02:25', '02:30', '02:35', '02:40',
               '02:45', '02:50', '02:55', '03:00', '03:05', '03:10', '03:15', '03:20', '03:25', '03:30', '03:35',
               '03:40', '03:45', '03:50', '03:55', '04:00', '04:05', '04:10', '04:15', '04:20', '04:25', '04:30',
               '04:35', '04:40', '04:45', '04:50', '04:55', '05:00', '05:05', '05:10', '05:15', '05:20', '05:25',
               '05:30', '05:35', '05:40', '05:45', '05:50', '05:55', '06:00', '06:05', '06:10', '06:15', '06:20',
               '06:25', '06:30', '06:35', '06:40', '06:45', '06:50', '06:55', '07:00', '07:05', '07:10', '07:15',
               '07:20', '07:25', '07:30', '07:35', '07:40', '07:45', '07:50', '07:55', '08:00', '08:05', '08:10',
               '08:15', '08:20', '08:25', '08:30', '08:35', '08:40', '08:45', '08:50', '08:55', '09:00', '09:05',
               '09:10', '09:15', '09:20', '09:25', '09:30', '09:35', '09:40', '09:45', '09:50', '09:55', '10:00',
               '10:05', '10:10', '10:15', '10:20', '10:25', '10:30', '10:35', '10:40', '10:45', '10:50', '10:55',
               '11:00', '11:05', '11:10', '11:15', '11:20', '11:25', '11:30', '11:35', '11:40', '11:45', '11:50',
               '11:55', '12:00', '12:05', '12:10', '12:15', '12:20', '12:25', '12:30', '12:35', '12:40', '12:45',
               '12:50', '12:55', '13:00', '13:05', '13:10', '13:15', '13:20', '13:25', '13:30', '13:35', '13:40',
               '13:45', '13:50', '13:55', '14:00', '14:05', '14:10', '14:15', '14:20', '14:25', '14:30', '14:35',
               '14:40', '14:45', '14:50', '14:55', '15:00', '15:05', '15:10', '15:15', '15:20', '15:25', '15:30',
               '15:35', '15:40', '15:45', '15:50', '15:55', '16:00', '16:05', '16:10', '16:15', '16:20', '16:25',
               '16:30', '16:35', '16:40', '16:45', '16:50', '16:55', '17:00', '17:05', '17:10', '17:15', '17:20',
               '17:25', '17:30', '17:35', '17:40', '17:45', '17:50', '17:55', '18:00', '18:05', '18:10', '18:15',
               '18:20', '18:25', '18:30', '18:35', '18:40', '18:45', '18:50', '18:55', '19:00', '19:05', '19:10',
               '19:15', '19:20', '19:25', '19:30', '19:35', '19:40', '19:45', '19:50', '19:55', '20:00', '20:05',
               '20:10', '20:15', '20:20', '20:25', '20:30', '20:35', '20:40', '20:45', '20:50', '20:55', '21:00',
               '21:05', '21:10', '21:15', '21:20', '21:25', '21:30', '21:35', '21:40', '21:45', '21:50', '21:55',
               '22:00', '22:05', '22:10', '22:15', '22:20', '22:25', '22:30', '22:35', '22:40', '22:45', '22:50',
               '22:55', '23:00', '23:05', '23:10', '23:15', '23:20', '23:25', '23:30', '23:35', '23:40', '23:45',
               '23:50', '23:55']


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def index(request):
    # data_list1 = requests.get(
    #     baseUrl + dataList, headers={'Authorization': 'Token be3d43142fa9a096398e67bb2f5a64da1d88cb1e',
    #                                  'Content-Type': 'application/json'})
    # data_list = data_list1.json()
    data_listtt = DCHubDetails.objects.all().order_by('created_at')[:10]
    # print(data_listtt)
    # print(list(data_listtt))
    dc_48_current1 = []
    dc_48_current2 = []
    dc_48_current3 = []
    dc_48_current4 = []
    dc_48_current5 = []
    dc_48_voltage1 = []
    dc_48_voltage2 = []
    battery_capacity = []
    bms_voltage = []
    bms_current = []
    pv1_voltage = []
    pv1_current = []
    created_at = []

    for d in data_listtt:
        dc_48_current1.append(d.dc_48_current1)
        dc_48_current2.append(d.dc_48_current2)
        dc_48_current3.append(d.dc_48_current3)
        dc_48_current4.append(d.dc_48_current4)
        dc_48_current5.append(d.dc_48_current5)
        dc_48_voltage1.append(d.dc_48_voltage1)
        dc_48_voltage2.append(d.dc_48_voltage2)
        battery_capacity.append(d.battery_capacity)
        bms_voltage.append(d.bms_voltage)
        bms_current.append(d.bms_current)
        pv1_voltage.append(d.pv1_voltage)
        pv1_current.append(d.pv1_current)
        # datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p')
        date = d.created_at
        created_at.append(datetime.datetime.strftime(date, '%b %d %Y %I:%M%p'))
        # print(created_at)
    data_list = serializers.serialize('json', data_listtt)
    # print(data_list)
    # charged = battery_capacity[-1]
    last_battery_data = DCHubDetails.objects.values('battery_capacity').last()
    print(last_battery_data)
    charged = last_battery_data['battery_capacity']
    # print(created_at)
    not_charged = 100 - charged
    battery_value = [charged, not_charged]
    context = {
        'dc_48_current1': dc_48_current1,
        'dc_48_current2': dc_48_current2,
        'dc_48_current3': dc_48_current3,
        'dc_48_current4': dc_48_current4,
        'dc_48_current5': dc_48_current5,
        'dc_48_voltage1': dc_48_voltage1[-1],
        'dc_48_voltage2': dc_48_voltage2[-1],
        'battery_capacity': battery_value,
        'bms_voltage': bms_voltage,
        'bms_current': bms_current,
        'pv1_voltage': pv1_voltage[-1],
        'pv1_current': pv1_current[-1],
        'created_at': created_at[-1],
        'created_at_all': created_at,
        'data_list': data_list,
    }
    if is_ajax(request=request):
        currentHtml = render_to_string('stats/currentChart.html', context, request=request)
        voltageHtml = render_to_string('stats/voltageChart.html', context, request=request)
        batteryHtml = render_to_string('stats/batteryChart.html', context, request=request)
        pv1Html = render_to_string('stats/pv1Chart.html', context, request=request)
        voltHt = render_to_string('stats/voltHt.html', context, request=request)
        chargeDetails = render_to_string('stats/chargeDetails.html', context, request=request)
        return JsonResponse(
            {'currentHtml': currentHtml, 'voltageHtml': voltageHtml, 'batteryHtml': batteryHtml, 'pv1Html': pv1Html,
             'voltHt': voltHt, 'chargeDetails': chargeDetails})
    else:
        return render(request, 'stats/index.html', context, )


def convert_to_localtime(utctime):
    fmt = '%b %d %Y %I:%M%p'
    utc = utctime.replace(tzinfo=pytz.UTC)
    # print(utctime+9:30)
    print(datetime.datetime.now(tzlocal()))
    localtz = utc.astimezone()
    return localtz.strftime(fmt)


def battery(request):
    created_at = []
    battery_data = []
    print('get get')
    # LOCAL_TIMEZONE = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo
    # print('local timezone', LOCAL_TIMEZONE)
    battery_data_reversed = reversed(DCHubDetails.objects.values('battery_capacity', 'created_at').order_by('-id')[:20])
    # date = reversed(DCHubDetails.objects.values('created_at').order_by('-id')[:20])
    for a in battery_data_reversed:
        # created_at.append(datetime.datetime.strftime(a['created_at'], '%b %d %Y %I:%M%p'))
        battery_data.append(a['battery_capacity'])
        date_test = convert_to_localtime(a['created_at'])
        # print(date_test)
        created_at.append(date_test)
    last_battery_data = DCHubDetails.objects.values('battery_capacity').last()
    charged = last_battery_data['battery_capacity']
    # print(created_at)

    not_charged = 100 - charged
    battery_value = [charged, not_charged]
    context = {'battery_data': battery_data,
               'battery_capacity': battery_value,
               'created_at': created_at,
               'unique_time': unique_time,

               }
    return render(request, 'stats/battery/batteryStat.html', context)


def batteryAjax(request):
    created_at = []
    battery_data = []
    print('abcc')

    if request.POST:
        print(request.POST)
        start_date = request.POST['start_date']
        start_time = request.POST['start_time']
        end_date = request.POST['end_date']
        end_time = request.POST['end_time']
        numberOfData = int(request.POST['numberOfData'])

        # print(start_date, start_time)
        st = datetime.datetime.strptime(start_time, '%H:%M').time()
        et = datetime.datetime.strptime(end_time, '%H:%M').time()
        sd = datetime.datetime.strptime(start_date, '%d/%m/%Y').date()
        ed = datetime.datetime.strptime(end_date, '%d/%m/%Y').date()

        sdt = datetime.datetime.combine(sd, st)
        edt = datetime.datetime.combine(ed, et)
        print(sdt, edt)

        search_battery_data = reversed(
            DCHubDetails.objects.filter(created_at__range=(sdt, edt)).values('battery_capacity', 'created_at').order_by(
                '-id')[:numberOfData])
        # print('search', search_battery_data)
        for a in search_battery_data:
            # created_at.append(datetime.datetime.strftime(a['created_at'], '%b %d %Y %I:%M%p'))
            battery_data.append(a['battery_capacity'])
            date_test = convert_to_localtime(a['created_at'])
            # print(date_test)
            created_at.append(date_test)
        # print(battery_data, 'dlfkjal', created_at)
        last_battery_data = DCHubDetails.objects.values('battery_capacity').last()
        charged = last_battery_data['battery_capacity']
        # print(created_at)
        notCharged = 100 - charged
        battery_value = [charged, notCharged]
        context = {'battery_data': battery_data,
                   'battery_capacity': battery_value,
                   'created_at': created_at,
                   'unique_time': unique_time,
                   }
        if is_ajax(request=request):
            batteryGraph = render_to_string('stats/battery/batteryGraph.html', context, request=request)
            print('ajaxxxxx')
            return JsonResponse({'batteryGraph': batteryGraph})


def refresh(request):
    # data_list1 = requests.get(
    #     baseUrl + dataList, headers={'Authorization': 'Token be3d43142fa9a096398e67bb2f5a64da1d88cb1e',
    #                                  'Content-Type': 'application/json'})
    # data_list = data_list1.json()
    data_listtt = DCHubDetails.objects.all().order_by('-created_at')[:20]
    data_list = serializers.serialize('json', data_listtt)
    context = {
        'data_list': data_list,

    }
    if request.is_ajax():
        currentHtml = render_to_string('stats/currentChart.html', context, request=request)
        voltageHtml = render_to_string('stats/voltageChart.html', context, request=request)
        batteryHtml = render_to_string('stats/batteryChart.html', context, request=request)
        pv1Html = render_to_string('stats/pv1Chart.html', context, request=request)
    return JsonResponse(
        {'currentHtml': currentHtml, 'voltageHtml': voltageHtml, 'batteryHtml': batteryHtml, 'pv1Html': pv1Html})
