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

class Event(db.Model):
    """Details of an event."""

    __tablename__ = "events"

    event_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    date_time = db.Column(db.DateTime)
    city = db.Column(db.Unicode(128))
    state = db.Column(db.Unicode(2))
    latitude = db.Column(db.Integer)
    longitude = db.Column(db.Integer)
    shape = db.Column(db.Unicode(32))
    duration = db.Column(db.Unicode(32))
    event_description = db.Column(db.UnicodeText)
    event_url = db.Column(db.Unicode(256))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return ("<Event:  event_id={id} | location={city}, {state} | shape={shape}>"
                .format(id=self.event_id, city=self.city, state=self.state, shape=self.shape))

#####################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///ufo_reports'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will
    # leave you in a state of being able to work with the database
    # directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."