"""Models and database functions for UFO Heatmap project"""

from flask_sqlalchemy import SQLAlchemy

# This is the connection to the PostgreSQL database; we're getting
# this through the Flask-SQLAlchemy helper library.  On this, we can
# find the 'session' object, where we do most of our interactions
# (like committing, etc.)

# Subclassing from SQLAlchemy
# class UnicodeSQLAlchemy(SQLAlchemy):
#     def apply_driver_hacks(self, app, info, options):
#         options.update({
#             'client_encoding': 'utf8'
#         })
#         super(UnicodeSQLAlchemy, self).apply_driver_hacks(app, info, options)


db = SQLAlchemy()


#####################################################################
# Model definitions

class User(db.Model):
    """User of UFO email list."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.Unicode(128))
    email = db.Column(db.Unicode(128))
    zipcode = db.Column(db.Integer)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return ("<User: user_id={id} | name={name} | email={email} | zipcode={zipcode}>"
                .format(id=self.user_id, name=self.name, email=self.email,
                        zipcode=self.zipcode))


class Event(db.Model):
    """Details of an event."""

    __tablename__ = "events"

    event_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    date_time = db.Column(db.DateTime)
    city = db.Column(db.Unicode(128))
    state = db.Column(db.Unicode(2))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    shape = db.Column(db.Unicode(32))
    duration = db.Column(db.Unicode(32))
    event_description = db.Column(db.UnicodeText)
    event_url = db.Column(db.Unicode(256))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return ("<Event:  event_id={id} | location={city}, {state} | shape={shape}>"
                .format(id=self.event_id, city=self.city, state=self.state, shape=self.shape))


class CityPop(db.Model):
    """Details of a city with population."""

    __tablename__ = "city_pops"

    city_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    city = db.Column(db.Unicode(128))
    state = db.Column(db.Unicode(128))
    population = db.Column(db.Integer)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return ("<Location={city}, {state} | population={population}>"
                .format(city=self.city,
                        state=self.state,
                        population=self.population))


def example_data():
    """Create some sample data."""

    # Add sample events and population data
    event1 = Event(date_time='1997-03-22 22:30:00', city='Stevens Point',
                   state='WI', latitude=44.5235773740005,
                   longitude=-89.5745569059997, shape='Crescent',
                   duration='1 1/2  Hours',
                   event_description='A hazey orange object hovered in the evening sky.It moved, in what looked like, a crescent shapefrom the upper North-East to the North-',
                   event_url='http://www.nuforc.org/webreports/002/S02095.html')
    event2 = Event(date_time='1996-06-24 00:30:00', city='Aurora', state='CO',
                   latitude=39.7294282970005, longitude=-104.83192,
                   shape='changed', duration='1 hour',
                   event_description='Obj. hovered 100 ft above car.  Red, blue lights on corners.  Changed shape from cube to pyramid to triangle.  Landed 800 ft away.',
                   event_url='http://www.nuforc.org/webreports/001/S01460.html')
    event3 = Event(date_time='2015-10-28 23:00:00', city='Baldwin Park',
                   state='CA', latitude=34.0852866460004,
                   longitude=-117.960899962, shape='Cross', duration='30',
                   event_description='((HOAX??))  It was like a cross with angle arms one bright light and red light above it. It was outside and I saw it, shocked.',
                   event_url='http://www.nuforc.org/webreports/123/S123214.html')


    city1 = CityPop(city='Abbeville city', state='Alabama', population=2688,
                    latitude=31.5667566350004, longitude=-85.2526589219997)
    city2 = CityPop(city='Adamsville city', state='Alabama', population=4522,
                    latitude=33.6063671440004, longitude=-86.9744581329996)
    city3 = CityPop(city='Addison town', state='Alabama', population=756,
                    latitude=34.2020062880005, longitude=-87.1762787239996)

    user1 = User(name='Charley', email='charley@gmail.com', zipcode=94596)
    user2 = User(name='Alex', email='alex@mac.com', zipcode=77040)
    user3 = User(name='Leila', email='leila@kitty.com', zipcode=70808)

    db.session.add_all([event1, event2, event3, city1, city2, city3,
                        user1, user2, user3])
    db.session.commit()

#####################################################################
# Helper functions

def connect_to_db(app, None):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri or 'postgresql:///ufo_reports'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)
    print "Connected to DB."


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will
    # leave you in a state of being able to work with the database
    # directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."