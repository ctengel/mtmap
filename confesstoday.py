#!/usr/bin/env python3

import core
import sys
import myconfig
import datetime

mycore = core.MTMap(myconfig.key, myconfig.cacheuri, myconfig.url)
myloc = core.Location(sys.argv[1])
#allchurches = mycore.find_churches(myloc)
#for i in allchurches:
#    print(i.name)
allmasses = mycore.mass_now(myloc, (datetime.datetime.now()-datetime.timedelta(hours=1), datetime.datetime.combine(datetime.date.today(),datetime.time(23,59,59))), svctyp='Confessions', dist=30)
for i in allmasses:
    print(i[0].name, i[0].addr, i[0].zipc, i[1]['time_start'], i[0].fullmto['distance'])
