#!/usr/bin/env python3

import gmapi
import gmapi.config as config
import cache
import sys

mycache = cache.Cache(config.cacheuri)
myapi = gmapi.GoogleMaps(mycache, config.key)
o = myapi.geocode(sys.argv[1])
print('Lat, Lng: %s, %s' % (o['lat'], o['lng']))
zp = myapi.geouncode(o['lat'], o['lng'])
print('Zip: %s' % zp)
print('TZ: %s' % myapi.timezone(o['lat'], o['lng']))
