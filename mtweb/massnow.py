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
    mtc = get_mtc()
    myloc = Location(zipcode)
    allmasses = mtc.mass_now(myloc, (datetime.datetime.now(datetime.timezone.utc)-datetime.timedelta(minutes=30), datetime.datetime.now(datetime.timezone.utc)+datetime.timedelta(hours=2)))
    masses = [{'name': i[0].name, 'addr': i[0].addr, 'zip': i[0].zipc, 'time': i[1]['time_start'], 'dist': i[0].fullmto['distance']} for i in allmasses]
    return render_template('massnow/display.html', masses=masses)
