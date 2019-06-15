
import urllib
import json


class GoogleMaps:
    
    def __init__(self, cache, key=None, url='https://maps.googleapis.com/maps/api/'):
        self.url = url
        self.key = key
        self.cache = cache

    def call(self, endpoint, params):
        params['key'] = self.key
        encoded = urllib.urlencode(params)
        data = self.cache.get_sync(self.url + endpoint + '/json?' + encoded)
        return json.loads(data)

    def geocode(self, address):

    def geouncode(self, lat, lon):
    

    
