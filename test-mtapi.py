#!/usr/bin/env python3

import mtapi
import mtapi.config as config
import json
import cache

mycache = cache.Cache(config.cacheuri)
myapi = mtapi.MassTimes(config.url, mycache)
data = myapi.call(config.lat, config.lon)
print(json.dumps(data, sort_keys=True, indent=4, separators=(',', ': ')))
