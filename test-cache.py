#!/usr/bin/env python3

import cache
import cache.config as config

mycache = cache.Cache(config.cacheuri)
print(mycache.get_sync(config.url))
