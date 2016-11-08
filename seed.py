"""Utility file to seed ufo_reports database from NUFORC data in seed_data/"""

from datetime import datetime
import geocoder
from sqlalchemy import func

from bs4 import BeautifulSoup
import lxml

from model import Event, connect_to_db, db
from server import app

# List of seed data files.
seed_data_files = ["/home/vagrant/src/project/seed_data/cross.html"]

# Imported files:


# Non-imported files:
# "/home/vagrant/src/project/seed_data/changed.html"
# "/home/vagrant/src/project/seed_data/crescent.html"
# "/home/vagrant/src/project/seed_data/delta.html"
# "/home/vagrant/src/project/seed_data/dome.html"
# "/home/vagrant/src/project/seed_data/changing.html"
# "/home/vagrant/src/project/seed_data/chevron.html",
# "/home/vagrant/src/project/seed_data/cigar.html",
# "/home/vagrant/src/project/seed_data/circle.html",
# "/home/vagrant/src/project/seed_data/cone.html",
# "/home/vagrant/src/project/seed_data/cylinder.html",
# "/home/vagrant/src/project/seed_data/diamond.html",
# "/home/vagrant/src/project/seed_data/disk.html",
# "/home/vagrant/src/project/seed_data/egg.html",
# "/home/vagrant/src/project/seed_data/fireball.html",
# "/home/vagrant/src/project/seed_data/flare.html",
# "/home/vagrant/src/project/seed_data/flash.html",
# "/home/vagrant/src/project/seed_data/formation.html",
# "/home/vagrant/src/project/seed_data/hexagon.html",
# "/home/vagrant/src/project/seed_data/light.html",
# "/home/vagrant/src/project/seed_data/other.html",
# "/home/vagrant/src/project/seed_data/oval.html",
# "/home/vagrant/src/project/seed_data/pyramid.html",
# "/home/vagrant/src/project/seed_data/rectangle.html",
# "/home/vagrant/src/project/seed_data/round.html",
# "/home/vagrant/src/project/seed_data/sphere.html",
# "/home/vagrant/src/project/seed_data/teardrop.html",
# "/home/vagrant/src/project/seed_data/triangle.html",
# "/home/vagrant/src/project/seed_data/triangular.html",
# "/home/vagrant/src/project/seed_data/unknown.html",
# "/home/vagrant/src/project/seed_data/unspecified.html"]

def get_lat_lng(city, state):
    """Geocode the given city (if any) and state."""
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

    Event.query.delete()

    num_skipped = 0
    total_added = 0

    for each_file in seed_data_files:

        print each_file

        # Create the soup object.
        soup = BeautifulSoup(open(each_file), "lxml")

        # Extract odd indices which contain the data we want.
        # Even indices contain a new line.
        # This creates a list of html strings.
        rows = soup.tbody.contents[1::2]

        i = 0

        for row in rows:

            city = row.contents[3].string
            state = row.contents[5].string

            if state:
                # Call the function defined above.
                lat_lng = get_lat_lng(city, state)

                if lat_lng:
                    # Unpackthe list.
                    latitude, longitude = lat_lng
                # Geocoding did not return a result.
                else:
                    print "tried geocoding, failed"
                    num_skipped += 1
                    continue
            # If no state was provided in the report.
            else:
                num_skipped += 1
                continue

            shape = row.contents[7].string
            duration = row.contents[9].string
            event_description = row.contents[11].string

            # date_time_raw:  u'3/11/16 19:30'
            # date_time is a datetime object.
            date_time_raw = row.contents[1].string

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

            # db.session.commit()

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
                # db.session.commit()
            i += 1
        print "i at end:", i
    # Once we're done, we'll commit our work.
    # db.session.commit()
    print "num_skipped: ", num_skipped
    print "total_added:", total_added

if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    load_events()
