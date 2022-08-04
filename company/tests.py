from django.test import TestCase
import requests as apiRequest
import json

# Create your tests here.

aus_address = apiRequest.get('https://darwinsolar-bucket.s3.amazonaws.com/Files/australia_address.geojson')
# print(aus_address.content.decode('utf-8'))
content = aus_address.content.decode('utf-8')
split = content.split('\n')
# print(split)
# print(len(split))
# print(content)
print('==============')
# for x in split:
#     print('-------------------')
#     # print(json.loads(x))
#     print('XXXXXxxxx')
# print(type(aus_address.content))
# print(json.loads(content))
for a in split:
    try:
        js = json.loads(a)
        print(js)
        ad_hash = js['properties']['hash']
        unit = js['properties']['unit']
        number = js['properties']['number']
        street = js['properties']['street']
        city = js['properties']['city']
        district = js['properties']['district']
        region = js['properties']['region']
        postcode = js['properties']['postcode']
        address_id = js['properties']['id']
        longitude = js['geometry']['coordinates'][0]
        latitude = js['geometry']['coordinates'][1]

        print(ad_hash)
        print(unit)
        print(number)
        print(street)
        print(city)
        print(district)
        print(region)
        print(postcode)
        print(address_id)
        print(longitude)
        print(latitude)
    except Exception as e:
        print(e)
    break
