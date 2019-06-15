
import googlemaps
import cache
import mtapi
# TODO import DB

class Location:
    def __init__(self, zipc=None, lat=None, lon=None, addr=None):
        if (lat and lon) or addr:
            self.exact = True
        else:
            self.exact = False
        if lat and lon:
            self.lat = lat
            self.lon = lon
        self.zipc = zipc
        self.addr = addr
        if zipc is None and addr is None and (lat is None or lon is None):
            raise Exception
    def is_exact(self):
        return self.exact
    def put_geocode(self, lat, lon):
        self.lat = lat
        self.lon = lon
    def rev_geocode(self, addr, zipc):
        self.addr = addr
        self.zipc = zipc
    def is_coded(self):
        return self.lat and self.lon


        

class Church(Location):
    def __init__(self, name, zipc=None, lat=None, lon=None, addr=None, mtobj=None, diocese=None):
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
        self.gmaps = googlemaps.Client(key=gmkey)
        mycache = cache.Cache(cacheuri)
        self.mtimes = mtapi.MassTimes(mturl, mycache)
        
    def find_route(self, dir_obj, exact=False):
        # check if already there
        # check if in db
        # Google Maps

    def find_churches(self, loc_obj, exact=False):
        # add dist params
        # check db
        if not exact and loc_obj.is_exact():
            lookup_obj = self.genericize(loc_obj)
        else:
            lookup_obj = loc_obj
        if not lookup_obj.is_coded():
            lookup_obj = self.fwd_geocode(lookup_obj)
        raw_churches = self.mtimes.get_radius(lookup_obj.lat, lookup_obj.lon)
        # include dist somehow
        # Church obj should have a constructor strictly from MT Output :)
        #return [Church(x['name'],x['church_address_postal_code'],x['latitude'],x['longitude'],{},x['church_worship_times'],x['diocese_name'] for x in raw_churches]

        # MassTimes

    def fwd_geocode(self, loc_obj):
        if not loc_obj.is_coded():
            # do stuff
            pass
        return (loc_obj.lat, loc_obj.lon)


    def rev_geocode(self, loc_obj):
        pass

    def genericize(self, loc_obj):
        # get zip from geocode (if not already)
        # set lat and long to zip lat and long and clear out 
