"""UFO reports."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, Event

from flask import jsonify


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "03J97OcS#!wN9Rq&tO&Czy"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined
app.jinja_env.auto_reload = True


@app.route('/')
def index():
    """Homepage."""

    return render_template("home.html")


@app.route('/events')
def map():
    """Show map of events."""

    return render_template("map.html")


@app.route('/events.json')
def event_info():
    """JSON information about events."""

    all_events = Event.query.all()
    events = {
        event.event_id: {
            "dateTime": event.date_time,
            "city": event.city,
            "state": event.state,
            "latitude": event.latitude,
            "longitude": event.longitude,
            "shape": event.shape,
            "duration": event.duration,
            "eventDescription": event.event_description,
            "eventUrl": event.event_url
        }
        for event in all_events}

    return jsonify(events)

#---------------------------------------------------------------------#

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    # app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(debug=True, host="0.0.0.0")
