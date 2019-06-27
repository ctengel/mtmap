

from urllib.parse import urlencode
import json

class MassTimes:

    def __init__(self, url, cache, maxage=604800):
        self.url = url
        self.cache = cache
        self.maxage = maxage
    
    def call(self, lat, lon, pg=1):
        params = {'lat': lat, 'long': lon, 'pg': pg}
        encoded = urlencode(params)
        data = self.cache.get_sync(self.url + '?' + encoded, self.maxage)
        return json.loads(data)

    def get_radius(self, lat, lon, mini=0, maxi=None):
        all_churches = []
        current_range = 0
        current_page = 1
        if maxi is not None and maxi < mini:
            raise Exception
        while current_range <= mini:
            these_churches = self.call(lat, lon, current_page)
            for this_church in these_churches:
                this_dist = float(this_church['distance'])
                if this_dist > current_range:
                    current_range = this_dist
                if maxi is None or this_dist <= maxi:
                    all_churches.append(this_church)
        return all_churches
