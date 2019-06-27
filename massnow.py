#!/usr/bin/env python3

import core
import sys
import myconfig

mycore = core.MTMap(myconfig.key, myconfig.cacheuri, myconfig.url)
myloc = core.Location(sys.argv[1])
allchurches = mycore.find_churches(myloc)
for i in allchurches:
    print(i.name)
