import mt_map

from flask import current_app, g

def get_mtc():
    if 'mtc' not in g:
        g.mtc = mt_map.MTMap(current_app.config['GKEY'], current_app.config['CACHEDB'], current_app.config['MTURL'])
    return g.mtc

def close_mtc(e=None):
    mtc = g.pop('mtc', None)
    if mtc is not None:
        mtc.close()

def init_app(app):
    app.teardown_appcontext(close_mtc)
