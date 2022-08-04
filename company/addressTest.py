import json

from company.models import AustraliaAddressModel

with open('../../../australia_address/australia_address.geojson', 'r') as f:
    for count, line in enumerate(f):
        print(line)
        js = json.loads(line)
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

        # print(ad_hash)
        # print(unit)
        # print(number)
        # print(street)
        # print(city)
        # print(district)
        # print(region)
        # print(postcode)
        # print(address_id)
        # print(longitude)
        # print(latitude)
        try:
            created = AustraliaAddressModel.objects.create(hash=ad_hash, unit=unit, number=number, street=street, city=city, district=district, state=region, postcode=postcode, add_original_id=address_id, longitude=longitude, latitude=latitude)
            if created:
                print(count, 'address created')
        except Exception as e:
            print('creation error with =>', e)

        # if count > 6:
        #     break
        # break
print('Total Lines', count + 1)
