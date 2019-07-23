
#import googlemaps
import gmapi
import cache
import mtapi
# TODO import DB
import re
import datetime

class Location:
    def __init__(self, zipc=None, lat=None, lon=None, addr=None):
        if (lat and lon) or addr:
            self.exact = True
        else:
            self.exact = False
        if lat and lon:
            self.lat = lat
            self.lon = lon
        else:
            self.lat = None
            self.lon = None
        self.zipc = zipc
        self.addr = addr
        if zipc is None and addr is None and (lat is None or lon is None):
            raise Exception
    def is_exact(self):
        return self.exact
    def put_geocode(self, lat, lng):
        self.lat = lat
        self.lon = lng
    def rev_geocode(self, addr, zipc):
        self.addr = addr
        self.zipc = zipc
    def is_coded(self):
        return self.lat and self.lon


        

class Church(Location):
    def __init__(self, name, zipc=None, lat=None, lon=None, addr=None, mtobj=None, diocese=None, fullmto=None):
        # TODO better way to inherit loc constructor
        if ((lat is None or lon is None) and addr is None) or name is None:
            raise Exception
        self.exact = True
        self.name = name
        self.mtobj = mtobj
        self.diocese = diocese
        self.addr = addr
        self.zipc = zipc
        if lat and lon:
            self.lat = lat
            self.lon = lon
        self.fullmto = fullmto
        if not addr and fullmto:
            self.addr = "%s, %s, %s" % (fullmto['church_address_street_address'], fullmto['church_address_city_name'], fullmto['church_address_providence_name'])
    def masses_in_range(self, timerange, svctyp):
        rtobj = []
        # TODO consider end time in range also & more sophisticated
        dow = timerange[0].strftime('%A')
        start = timerange[0].time()
        end = timerange[1].time()
        for i in self.mtobj:
            if i['day_of_week'] and re.match(dow, i['day_of_week']):
                to = datetime.time(* [int(x) for x in i['time_start'].split(':')])
                if start <= to and end >= to:
                    if not svctyp or svctyp == i['service_typename']:
                        rtobj.append((self, i))
        return rtobj



class Directions:
    def __init__(self, loc_array=None, dur_array=None, dist_array=None, polyline_arrays=None):
        # TODO implement multipoint
        raise Exception

class SingleDirections(Directions):
    def __init__(self, start, finish, dist=None, dur=None, polylines=None):
        self.start = start
        self.finish = finish
        self.dist = dist
        self.dur = dur
        self.polylines = polylines


class MTMap:
    def __init__(self, gmkey, cacheuri, mturl):
        # TODO add DB
        # TODO use googlemaps my gmapi???
        #self.gmaps = googlemaps.Client(key=gmkey)
        self.mycache = cache.Cache(cacheuri, 15)
        self.mtimes = mtapi.MassTimes(mturl, self.mycache)
        self.gmaps = gmapi.GoogleMaps(self.mycache, gmkey)
        
    def find_route(self, dir_obj, exact=False):
        # check if already there
        # check if in db
        # Google Maps
        pass

    def find_churches(self, loc_obj, exact=False, dist=None):
        # add dist params
        # check db
        if not exact:
            lookup_obj = self.genericize(loc_obj)
        else:
            lookup_obj = loc_obj
        self.fwd_geocode(lookup_obj)
        if dist is None:
            mini=0
            maxi=None
        else:
            mini=dist
            maxi=dist
        raw_churches = self.mtimes.get_radius(lookup_obj.lat, lookup_obj.lon, maxi=maxi, mini=mini)
        # include dist somehow
        # Church obj should have a constructor strictly from MT Output :)
        return [Church(x['name'],x['church_address_postal_code'],x['latitude'],x['longitude'],{},x['church_worship_times'],x['diocese_name'],x) for x in raw_churches]

    def mass_now(self, loc_obj, timespan, dist=None, svctyp=None):
        churches = self.find_churches(loc_obj, dist=dist)
        rtobj = []
        for i in churches:
            rtobj = rtobj + i.masses_in_range(timespan, svctyp)
        rtobj.sort(key=lambda x: x[1]['time_start'])
        return rtobj



    def fwd_geocode(self, loc_obj):
        if not loc_obj.is_coded():
            loc_obj.put_geocode(**self.gmaps.geocode(loc_obj.zipc))
        #return (loc_obj.lat, loc_obj.lon)


    def rev_geocode(self, loc_obj):
        if not loc_obj.zipc:
            loc_obj.rev_geocode(None, self.gmaps.geouncode(loc_obj.lat, loc_obj.lon))


    def genericize(self, loc_obj):
        # get zip from geocode (if not already)
        # set lat and long to zip lat and long and clear out 
        # TODO now
        if not loc_obj.is_exact():
            return loc_obj
        self.rev_geocode(loc_obj)
        new_loc = Location(loc_obj.zipc)
        return new_loc

    def close(self):
        self.mycache.close()
