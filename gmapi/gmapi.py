
from urllib.parse import urlencode
import json


class GoogleMaps:
    
    def __init__(self, cache, key=None, url='https://maps.googleapis.com/maps/api/'):
        self.url = url
        self.key = key
        self.cache = cache

    def call(self, endpoint, params):
        params['key'] = self.key
        encoded = urlencode(params)
        data = self.cache.get_sync(self.url + endpoint + '/json?' + encoded)
        return json.loads(data)

    def geocode(self, address):
        return self.call('geocode', {'address': address})['results'][0]['geometry']['location']

    def geouncode(self, lat, lng):
        return list(filter(lambda x: ('postal_code' in x['types']), self.call('geocode', {'latlng': ','.join([str(lat), str(lng)])})['results'][0]['address_components']))[0]['short_name']

    def timezone(self, lat, lng):
        return self.call('timezone', {'location': ','.join([str(lat), str(lng)]), 'timestamp': 0})['timeZoneId']

