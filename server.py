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

DAYS_OF_WEEK = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday",
                "Friday", "Saturday"]


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
    events_per_capita_states = ([float(states_events_and_pops[i][0]) * 100000
                                / states_events_and_pops[i][1]
                                for i in range(len(states_events_and_pops))])

    # write the json dictionary for the state: event/per capita state
    events_per_cap = {
        "labels": STATES,
        "datasets": [
            {
                "data": events_per_capita_states,
                "backgroundColor": [
                    "#000000", "#FFFF00", "#1CE6FF", "#FF34FF", "#FF4A46",
                    "#008941", "#006FA6", "#A30059", "#FFDBE5", "#7A4900",
                    "#0000A6", "#63FFAC", "#B79762", "#004D43", "#8FB0FF",
                    "#997D87", "#5A0007", "#809693", "#FEFFE6", "#1B4400",
                    "#4FC601", "#3B5DFF", "#4A3B53", "#FF2F80", "#61615A",
                    "#BA0900", "#6B7900", "#00C2A0", "#FFAA92", "#FF90C9",
                    "#B903AA", "#D16100", "#DDEFFF", "#000035", "#7B4F4B",
                    "#A1C299", "#300018", "#0AA6D8", "#013349", "#00846F",
                    "#372101", "#FFB500", "#C2FFED", "#A079BF", "#CC0744",
                    "#C0B9B2", "#C2FF99", "#001E09", "#00489C", "#6F0062",
                    "#0CBD66", "#EEC3FF", "#456D75", "#B77B68", "#7A87A1",
                    "#788D66", "#885578", "#FAD09F", "#FF8A9A", "#D157A0",
                    "#BEC459", "#456648", "#0086ED", "#886F4C", "#34362D",
                    "#B4A8BD", "#00A6AA", "#452C2C", "#636375", "#A3C8C9",
                    "#FF913F", "#938A81", "#575329", "#00FECF", "#B05B6F",
                    "#8CD0FF", "#3B9700", "#04F757", "#C8A1A1", "#1E6E00",
                    "#7900D7", "#A77500", "#6367A9", "#A05837", "#6B002C",
                    "#772600", "#D790FF", "#9B9700", "#549E79", "#FFF69F",
                    "#201625", "#72418F", "#BC23FF", "#99ADC0", "#3A2465",
                    "#922329", "#5B4534", "#FDE8DC", "#404E55", "#0089A3",
                    "#CB7E98", "#A4E804", "#324E72", "#6A3A4C"
                ]
            }
        ]
    }


    jsonified = jsonify(events_per_cap)
    print jsonified
    return jsonified


@app.route('/reports-each-day-of-week.json')
def reports_each_day_of_week():
    """JSON information about UFO reports for each day of the week"""

    # Query for all events
    all_events = Event.query.all()

    # Create a list of the day of the week for each event
    days_of_week = [event.date_time.weekday() for event in all_events]

    # Create a list of the count of events for each day of the week
    events_each_day = [days_of_week.count(i) for i in range(7)]

    # Construct the dictionary
    events_per_day_of_week = {
        "labels": DAYS_OF_WEEK,
        "datasets": [
            {
                "label": "Events per day of week",
                "backgroundColor": [
                    "#1f77b4", "#aec7e8", "#ff7f0e", "#ffbb78", "#2ca02c",
                    "#98df8a", "#d62728", "#ff9896", "#9467bd", "#c5b0d5",
                    "#8c564b", "#c49c94", "#e377c2", "#f7b6d2", "#7f7f7f",
                    "#c7c7c7", "#bcbd22", "#dbdb8d", "#17becf", "#9edae5",
                    "#1f77b4", "#aec7e8", "#ff7f0e", "#ffbb78", "#2ca02c",
                    "#98df8a", "#d62728", "#ff9896", "#9467bd", "#c5b0d5",
                    "#8c564b", "#c49c94", "#e377c2", "#f7b6d2", "#7f7f7f",
                    "#c7c7c7", "#bcbd22", "#dbdb8d", "#17becf", "#9edae5",
                    "#1f77b4", "#aec7e8", "#ff7f0e", "#ffbb78", "#2ca02c",
                    "#98df8a", "#d62728", "#ff9896", "#9467bd", "#c5b0d5",
                    "#8c564b", "#c49c94", "#e377c2", "#f7b6d2", "#7f7f7f",
                    "#c7c7c7", "#bcbd22", "#dbdb8d", "#17becf", "#9edae5",
                ],  # end of backgroundColor
                "borderColor": [
                    "#1f77b4", "#aec7e8", "#ff7f0e", "#ffbb78", "#2ca02c",
                    "#98df8a", "#d62728", "#ff9896", "#9467bd", "#c5b0d5",
                    "#8c564b", "#c49c94", "#e377c2", "#f7b6d2", "#7f7f7f",
                    "#c7c7c7", "#bcbd22", "#dbdb8d", "#17becf", "#9edae5",
                    "#1f77b4", "#aec7e8", "#ff7f0e", "#ffbb78", "#2ca02c",
                    "#98df8a", "#d62728", "#ff9896", "#9467bd", "#c5b0d5",
                    "#8c564b", "#c49c94", "#e377c2", "#f7b6d2", "#7f7f7f",
                    "#c7c7c7", "#bcbd22", "#dbdb8d", "#17becf", "#9edae5",
                    "#1f77b4", "#aec7e8", "#ff7f0e", "#ffbb78", "#2ca02c",
                    "#98df8a", "#d62728", "#ff9896", "#9467bd", "#c5b0d5",
                    "#8c564b", "#c49c94", "#e377c2", "#f7b6d2", "#7f7f7f",
                    "#c7c7c7", "#bcbd22", "#dbdb8d", "#17becf", "#9edae5",
                ],  # end of borderColor
                "borderWidth": 1,
                "data": events_each_day,
            }
        ]  # end of datasets
    }  # end of events_per_day_of_week

    jsonified = jsonify(events_per_day_of_week)
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
