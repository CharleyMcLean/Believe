"""Models and database functions for UFO Heatmap project"""

from flask_sqlalchemy import SQLAlchemy

# This is the connection to the PostgreSQL database; we're getting 
# this through the Flask-SQLAlchemy helper library.  On this, we can
# find the 'session' object, where we do most of our interactions
# (like committing, etc.)

db = SQLAlchemy()


#####################################################################
# Model definitions

class Event(db.Model):
    """Details of an event."""

    __tablename__ = "events"

    event_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    datetime = db.Column(db.DateTime)
    city = db.Column(db.String(128))
    state = db.Column(db.String(2))
    shape = db.Column(db.String(32))
    duration = db.Column(db.String(32))
    event_description = db.Column(db.UnicodeText)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return ("<Event:  event_id=%d | location=%s, %s | shape=%s>"
                % (self.event_id, self.city, self.state, self.shape))

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