"""Utility file to seed ufo_reports database from NUFORC data in seed_data/"""

import datetime
from sqlalchemy import func

from model import Event, connect_to_db, db
from server import app

# List of seed data files.
seed_data_files = ["changed.html", "changing.html", "chevron.html",
                   "cigar.html", "circle.html", "cone.html",
                   "crescent.html", "cross.html", "cylinder.html",
                   "delta.html", "diamond.html", "disk.html",
                   "dome.html", "egg.html", "fireball.html",
                   "flare.html", "flash.html", "formation.html",
                   "hexagon.html", "light.html", "other.html",
                   "oval.html", "pyramid.html", "rectangle.html",
                   "round.html", "sphere.html", "teardrop.html",
                   "triangle.html", "triangular.html", "unknown.html",
                   "unspecified.html"]


def load_events(files):
    """Load events from seed_data files into database"""

    for each_file in files:

        # Create the soup object.
        soup = BeautifulSoup(open(each_file), "lxml")

        # Extract odd indices which contain the data we want.
        # Even indices contain a new line.
        # This creates a list of html strings.
        rows = soup.tbody.contents[1::2]

        for row in rows:
            # For each row of html, extract the event details.
            date_time = row.contents[1].string
            city = row.contents[3].string
            state = row.contents[5].string
            shape = row.contents[7].string
            duration = row.contents[9].string
            event_description = row.contents[11].string

            # This returns the html element containing the link, which we're
            # grabbing the 'href' value from.
            end_of_url = row.find('a', href=True)['href']
           
            # Construct the full url.
            event_url = 'http://www.nuforc.org/webreports/' + end_of_url

            event = Event(date_time=date_time,
                          city=city,
                          state=state,
                          shape=shape,
                          duration=duration,
                          event_description=event_description,
                          event_url=event_url)

            # Add the event to the session.
            db.session.add(event)

    # Once we're done, we'll commit our work.
    db.session.commit()
