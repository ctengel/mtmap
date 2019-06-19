

import time
import sqlalchemy
import sqlalchemy.ext.declarative
import sqlalchemy.orm
import requests
#import datetime

Base = sqlalchemy.ext.declarative.declarative_base()

class CachedItem(Base):
    # TODO need to add field for status
    # TODO add hitcounter
    __tablename__ = 'cache'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    url = sqlalchemy.Column(sqlalchemy.String)
    cached = sqlalchemy.Column(sqlalchemy.Integer)
    data = sqlalchemy.Column(sqlalchemy.Text)
    hit = sqlalchemy.Column(sqlalchemy.Integer)
    def __repr__(self):
        return "<CachedItem(url='%s')>" % (self.url)


class Cache:
    # TODO better async; one func

    def __init__(self, cachefile, limit=0):
        self.engine = sqlalchemy.create_engine(cachefile)
        Base.metadata.create_all(self.engine)
        self.Session = sqlalchemy.orm.sessionmaker(bind=self.engine)
        self.limit = limit
        self.lastpull = int(time.time())

    def rate_limit(self, now=None):
        if now is None:
            now = time.time()
        if now < self.lastpull + self.limit:
            time.sleep(self.lastpull + self.limit - now)
            now = time.time()
        self.lastpull = now
        return now

    def purge_old(self, maxage):
        pass

    def purge_unused(self, maxsize):
        pass

    def get_sync(self, url, maxage=None):
        now = time.time()
        session = self.Session()
        dbobj = session.query(CachedItem).filter_by(url=url).first()
        if dbobj and (maxage is None or dbobj.cached > now - maxage):
            dbobj.hit = now
            session.commit()
            return dbobj.data
        else:
            now = self.rate_limit(now)
            data = requests.get(url).text
            if dbobj:
                dbobj.data = data
                dbobj.cached = now
                dbobj.hit = now
            else:
                dbobj = CachedItem(url=url,data=data,cached=now,hit=now)
                session.add(dbobj)
            session.commit()
            return data

    def get_async(self, url, maxage=None, ican=False):
        pass

    def by_id(self, id):
        pass
