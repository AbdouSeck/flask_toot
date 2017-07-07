import json

import geocoder
import urllib
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    pwdhash = db.Column(db.String(54))

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name.title()
        self.last_name = last_name.title()
        self.email = email.lower()
        self.set_password(password)

    def set_password(self, password):
        self.pwdhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)


class Place(object):
    @staticmethod
    def meters_to_walking_time(meters):
        # 80 meters is one minute walking time
        return int(meters / 80)

    @staticmethod
    def wiki_path(slug):
        return urllib.parse.urljoin("http://en.wikipedia.org/wiki/", slug.replace(' ', '_'))

    @staticmethod
    def address_to_latlng(address):
        g = geocoder.google(address)
        return g.lat, g.lng

    def query(self, address):
        lat, lng = self.address_to_latlng(address)
        main_url = "https://en.wikipedia.org/w/api.php?action=query&list=geosearch&gsradius=5000&"
        query_url = "{0}gscoord={1}%7C{2}&gslimit=20&format=json".format(main_url, lat, lng)
        g = urllib.request.urlopen(query_url)
        results = g.read()
        g.close()

        data = json.loads(results)

        places = []
        for place in data['query']['geosearch']:
            name = place['title']
            meters = place['dist']
            lat = place['lat']
            lng = place['lon']

            wiki_url = self.wiki_path(name)
            walking_time = self.meters_to_walking_time(meters)

            d = {
                'name': name,
                'url': wiki_url,
                'time': walking_time,
                'lat': lat,
                'lng': lng
            }

            places.append(d)

        return places
