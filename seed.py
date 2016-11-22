"""Utility file to seed ufo_reports database from NUFORC data in seed_data/"""

from datetime import datetime
import geocoder
from sqlalchemy import func

from bs4 import BeautifulSoup
import lxml

from model import Event, connect_to_db, db
from server import app

# List of seed data files.
seed_data_files = ["/home/vagrant/src/project/seed_data/triangle.html"]

# Imported files:
# "/home/vagrant/src/project/seed_data/changed.html" 0 skipped, 1 added
# "/home/vagrant/src/project/seed_data/changing.html" 461 skipped, 2139 added
# "/home/vagrant/src/project/seed_data/chevron.html" 180 skipped, 1048 added
# "/home/vagrant/src/project/seed_data/cigar.html" 515 skipped, 2095 added
# "/home/vagrant/src/project/seed_data/circle.html"
# "/home/vagrant/src/project/seed_data/cone.html" 97 skipped, 352 added
# "/home/vagrant/src/project/seed_data/crescent.html" 1 skipped, 1 added
# "/home/vagrant/src/project/seed_data/cross.html" 57 skipped, 271 added
# "/home/vagrant/src/project/seed_data/cylinder.html" 312 skipped, 1342 added
# "/home/vagrant/src/project/seed_data/delta.html" 1 skipped, 7 added
# "/home/vagrant/src/project/seed_data/diamond.html", 314 skipped, 1256 added
# "/home/vagrant/src/project/seed_data/disk.html" at least 1239 skipped, 3623 added
# "/home/vagrant/src/project/seed_data/dome.html" 1 skipped, 0 added
# "/home/vagrant/src/project/seed_data/egg.html" 222 skipped, 749 added
# "/home/vagrant/src/project/seed_data/fireball.html" ???? seems like a 10th seeded
# "/home/vagrant/src/project/seed_data/flare.html" 0 skipped, 1 added
# "/home/vagrant/src/project/seed_data/flash.html" 318 skipped, 1536 added
# "/home/vagrant/src/project/seed_data/formation.html" 567 skipped, 2732 failed
# "/home/vagrant/src/project/seed_data/hexagon.html" 0 skipped, 1 added
# "/home/vagrant/src/project/seed_data/light.html"
# "/home/vagrant/src/project/seed_data/oval.html" at least 580 skipped, 1875 added
# "/home/vagrant/src/project/seed_data/pyramid.html" 0 skipped, 1 added
# "/home/vagrant/src/project/seed_data/rectangle.html" at least 285 skipped, 1068 added
# "/home/vagrant/src/project/seed_data/round.html" 0 skipped, 2 added
# "/home/vagrant/src/project/seed_data/sphere.html" at least 437 skipped, 1154 added
# "/home/vagrant/src/project/seed_data/teardrop.html" 197 skipped, 786 added
# "/home/vagrant/src/project/seed_data/triangular.html" 1 skipped, 0 added
# "/home/vagrant/src/project/seed_data/unspecified.html" 908 skipped, 2508 added


# Non-imported files:
# "/home/vagrant/src/project/seed_data/other.html", 7416
# , 10183
# "/home/vagrant/src/project/seed_data/unknown.html", 7610

def get_lat_lng(city, state):
    """Geocode the given city (if any) and state."""
    # Printing for debugging purposes.
    print city, state
    #if city is given, include it in the geocoding
    if city:
        geocode_result = geocoder.arcgis(city + ", " + state)
    #otherwise, just get a generic lat/lng for the state
    else:
        geocode_result = geocoder.arcgis(state)

    #status will be "OK" if a usable result comes back; if so, return it
    status = geocode_result.json["status"]
    if status == "OK":
        lat = geocode_result.json["lat"]
        lng = geocode_result.json["lng"]
        return lat, lng
    #otherwise, return None
    else:
        return None


def load_events():
    """Load events from seed_data files into database"""
    # Only use this line if starting the database from scratch.
    # Otherwise DO NOT uncomment.
    # Event.query.delete()

    # Start a count for the number skipped and added while seeding the db.
    num_skipped = 0
    total_added = 0

    # Iterate through the file(s).
    for each_file in seed_data_files:
        # Print statement for debugging.
        print each_file

        # Create the soup object.
        soup = BeautifulSoup(open(each_file), "lxml")

        # Extract odd indices which contain the data we want.
        # Even indices contain a new line.
        # This creates a list of html strings.
        rows = soup.tbody.contents[1::2]

        # Start a counter for the number of reports cycled through.
        i = 0
        # Iterate through each row of the file.
        for row in rows:
            # Capture city and state in variables.
            city = row.contents[3].string
            state = row.contents[5].string

            # If a state exists, call the get_lat_lng function defined above.
            if state:
                lat_lng = get_lat_lng(city, state)
                # If lat_lng exists, capture the values of latitude and longitude.
                if lat_lng:
                    # Unpack the list.
                    latitude, longitude = lat_lng
                # If lat_lng is None, then geocoding did not return a result.
                else:
                    print "tried geocoding, failed"
                    num_skipped += 1
                    continue
            # If no state was provided in the report.
            # Don't want to include reports with city only, as there are 
            # sometimes more than one state associated with a city name.
            else:
                num_skipped += 1
                continue

            # Capture the values of shape, duration, and event description.
            shape = row.contents[7].string
            duration = row.contents[9].string
            event_description = row.contents[11].string

            # Capture the value of the date/time of the event.
            # date_time_raw:  u'3/11/16 19:30'
            # date_time is a datetime object.
            date_time_raw = row.contents[1].string

            # Convert the date/time info to a datetime object.
            # If the date and/or time are missing or in the wrong format,
            # it will be skipped and the session will rollback to prevent errors.
            try:
                date_time = datetime.strptime(date_time_raw, '%m/%d/%y %H:%M')
            except BaseException as e:
                print str(e)
                num_skipped += 1
                db.session.rollback()
                continue

            # This returns the html element containing the link, which we're
            # grabbing the 'href' value from. Then construct the full url.
            end_of_url = row.find('a', href=True)['href']
            event_url = 'http://www.nuforc.org/webreports/' + end_of_url

            event = Event(date_time=date_time,
                          city=city,
                          state=state,
                          latitude=latitude,
                          longitude=longitude,
                          shape=shape,
                          duration=duration,
                          event_description=event_description,
                          event_url=event_url)

            # print event
            # Add the event to the session.
            db.session.add(event)

            try:
                db.session.commit()
                total_added += 1
            except BaseException as e:
                print str(e)
                num_skipped += 1
                db.session.rollback()
                continue

            # provide some sense of progress
            if i % 100 == 0:
                print i
            i += 1

        print "i at end:", i
    # Once we're done, we'll commit our work.
    # db.session.commit()
    print "num_skipped: ", num_skipped
    print "total_added:", total_added

#######################################################################

if __name__ == "__main__":
    connect_to_db(app)
    # db.create_all()

    load_events()
