#!/usr/bin/env python3

import mt_map
import sys
import myconfig
import datetime

mycore = mt_map.MTMap(myconfig.key, myconfig.cacheuri, myconfig.url)
myloc = mt_map.Location(sys.argv[1])
#allchurches = mycore.find_churches(myloc)
#for i in allchurches:
#    print(i.name)
allmasses = mycore.mass_now(myloc, (datetime.datetime.now()-datetime.timedelta(minutes=30), datetime.datetime.now()+datetime.timedelta(hours=2)))
for i in allmasses:
    print(i[0].name, i[0].addr, i[0].zipc, i[1]['time_start'], i[0].fullmto['distance'])
