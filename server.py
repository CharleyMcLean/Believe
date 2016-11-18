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


# define global variables for states
STATES_ABBREV = ['AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL',
                 'GA', 'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA',
                 'MD', 'ME', 'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE',
                 'NH', 'NJ', 'NM', 'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'RI',
                 'SC', 'SD', 'TN', 'TX', 'UT', 'VA', 'VT', 'WA', 'WI',
                 'WV', 'WY']

STATES = ['Alaska', 'Alabama', 'Arkansas', 'Arizona', 'California', 'Colorado',
          'Connecticut', 'District of Columbia', 'Delaware', 'Florida',
          'Georgia', 'Hawaii', 'Iowa', 'Idaho', 'Illinois', 'Indiana', 'Kansas',
          'Kentucky', 'Louisiana', 'Massachusetts', 'Maryland', 'Maine',
          'Michigan', 'Minnesota', 'Missouri', 'Mississippi', 'Montana',
          'North Carolina', 'North Dakota', 'Nebraska', 'New Hampshire',
          'New Jersey', 'New Mexico', 'Nevada', 'New York', 'Ohio', 'Oklahoma',
          'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina',
          'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Virginia', 'Vermont',
          'Washington', 'Wisconsin', 'West Virginia', 'Wyoming']


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


@app.route('/reports-per-capita.json')
def per_capita_info():
    """JSON information about UFO reports per capita for each state"""

    # Can add in code to account for states with no data (for testing)

    # [236L, 455L, ...]
    states_events_counts = (
        [db.session.query(Event).filter(Event.state == state).count()
         for state in STATES_ABBREV])

    # [234234, 25345, ...]
    states_pop_counts = []
    for state in STATES:
        sum_of_peeps = 0
        pops = db.session.query(CityPop).filter(CityPop.state == state).all()
        for city in pops:
            sum_of_peeps += city.population
        states_pop_counts.append(sum_of_peeps)

    # [(207L, 2342), ...]
    states_events_and_pops = zip(states_events_counts, states_pop_counts)

    # Divide the # of events in each state by the population of that state.
    # import pdb; pdb.set_trace()
    events_per_capita_states = ([float(states_events_and_pops[i][0])
                                / states_events_and_pops[i][1]
                                for i in range(len(states_events_and_pops) - 1)])

    # write the json dictionary for the state: event/per capita state
    events_per_cap = {}
    for i in range(len(events_per_capita_states)):
        events_per_cap[STATES[i]] = events_per_capita_states[i]

    jsonified = jsonify(events_per_cap)
    print jsonified
    return jsonified


############################################################################
# Not currently using this route.  If I choose to in the future, need to
# uncomment out related code and script src in map.html.

@app.route('/newsletter-signup', methods=['POST'])
def signup():
    """Signup for a newsletter."""

    # Get form variables.
    name = request.form.get("name")
    email = request.form.get("email")
    zipcode = int(request.form.get("zipcode"))

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

        # Create a variable to store the status to be shown with JS.
        status = "Your email %s has been added to our newsletter distribution\
                 list! We thank you for believing." % email

    else:
        status = "Your email %s has already been added to our newsletter\
                 distribution list! We thank you for believing." % email

    return status

#---------------------------------------------------------------------#

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    # app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(debug=True, host="0.0.0.0")
