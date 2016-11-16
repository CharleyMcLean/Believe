"""UFO reports."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, Event, CityPop, User

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


@app.route('/newsletter-signup', methods=['POST'])
def signup():
    """Signup for a newsletter."""

    # Get form variables.
    name = request.form.get("name")
    email = request.form["email"]  # user .get()
    zipcode = int(request.form["zipcode"])

    # assume the worst
    # assume they gave you a zipcode which is the txt of hamlet
    # assum name/email is empty

    # Check if the user exists in the database, aka if they've
    # already signed up for emails.
    if not User.query.filter_by(email=email).first():
        # If user does not exist in the db, create, add, and commit the user.
        new_user = User(name=name, email=email, zipcode=zipcode)
        db.session.add(new_user)
        db.session.commit()

        # Create a variable to store the status and flash a success message.
        status = "User successfully added to database."
        flash("Your email %s has been added to our newsletter distribution list! We thank you for believing." % email)

    else:
        status = "User already signed up for newsletter."
        flash("Your email %s has been added to our newsletter distribution list! We thank you for believing." % email)

    return status


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
    jsonified = jsonify(events)
    print jsonified
    return jsonified


@app.route('/population.json')
def city_pop_info():
    """JSON information about population."""

    all_city_pops = CityPop.query.all()
    city_pops = {
        city_pop.city_id: {
            "city": city_pop.city,
            "state": city_pop.state,
            "population": city_pop.population,
            "latitude": city_pop.latitude,
            "longitude": city_pop.longitude,
        }
        for city_pop in all_city_pops}
    jsonified = jsonify(city_pops)
    print jsonified
    return jsonified

#---------------------------------------------------------------------#

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    # app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(debug=True, host="0.0.0.0")
