from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from mtweb.mtc import get_mtc

from mt_map import Location

import datetime

bp = Blueprint('massnow', __name__)

@bp.route('/')
def find():
    return render_template('massnow/find.html')

@bp.route('/mtn')
def display():
    zipcode = request.args.get('zip')
    latlng = request.args.get('latlng')
    svctyp = request.args.get('svctyp')
    timing = request.args.get('timing')
    if timing == 'now':
        timespan = (datetime.datetime.now(datetime.timezone.utc)-datetime.timedelta(minutes=30), datetime.datetime.now(datetime.timezone.utc)+datetime.timedelta(hours=2))
    elif timing == 'rel':
        relhours = int(request.args.get('relhours'))
        timespan = (datetime.datetime.now(datetime.timezone.utc)-datetime.timedelta(minutes=30)+datetime.timedelta(hours=relhours), datetime.datetime.now(datetime.timezone.utc)+datetime.timedelta(hours=(2+relhours)))
    elif timing == 'abs':
        # TODO need to lookup zip code time zone to figure out what and then English string to this conversion
        pass
    else:
        # TODO really should just assume now
        assert False
    dist = int(request.args,get('dist'))
    if not svctyp:
        svctyp = 'Masses'
    if not dist:
        dist = None
    mtc = get_mtc()
    if latlng and zipcode == 'AUTO':
        lat, lon = tuple(latlng.split(','))
        myloc = Location(lat=lat, lon=lon)
    else:
        myloc = Location(zipcode)
    allmasses = mtc.mass_now(myloc, timespan, dist, svctyp)
    masses = [{'name': i[0].name, 'addr': i[0].addr, 'zip': i[0].zipc, 'time': i[1]['time_start'], 'dist': i[0].fullmto['distance']} for i in allmasses]
    return render_template('massnow/display.html', masses=masses)
