"""Utility file to seed ufo_reports database from NUFORC data in seed_data/"""

from datetime import datetime
from sqlalchemy import func

from bs4 import BeautifulSoup
import lxml

from model import Event, connect_to_db, db
from server import app

# List of seed data files.
seed_data_files = ["/home/vagrant/src/project/seed_data/changed.html",
                   "/home/vagrant/src/project/seed_data/changing.html",
                   "/home/vagrant/src/project/seed_data/chevron.html",
                   "/home/vagrant/src/project/seed_data/cigar.html",
                   "/home/vagrant/src/project/seed_data/circle.html",
                   "/home/vagrant/src/project/seed_data/cone.html",
                   "/home/vagrant/src/project/seed_data/crescent.html",
                   "/home/vagrant/src/project/seed_data/cross.html",
                   "/home/vagrant/src/project/seed_data/cylinder.html",
                   "/home/vagrant/src/project/seed_data/delta.html",
                   "/home/vagrant/src/project/seed_data/diamond.html",
                   "/home/vagrant/src/project/seed_data/disk.html",
                   "/home/vagrant/src/project/seed_data/dome.html",
                   "/home/vagrant/src/project/seed_data/egg.html",
                   "/home/vagrant/src/project/seed_data/fireball.html",
                   "/home/vagrant/src/project/seed_data/flare.html",
                   "/home/vagrant/src/project/seed_data/flash.html",
                   "/home/vagrant/src/project/seed_data/formation.html",
                   "/home/vagrant/src/project/seed_data/hexagon.html",
                   "/home/vagrant/src/project/seed_data/light.html",
                   "/home/vagrant/src/project/seed_data/other.html",
                   "/home/vagrant/src/project/seed_data/oval.html",
                   "/home/vagrant/src/project/seed_data/pyramid.html",
                   "/home/vagrant/src/project/seed_data/rectangle.html",
                   "/home/vagrant/src/project/seed_data/round.html",
                   "/home/vagrant/src/project/seed_data/sphere.html",
                   "/home/vagrant/src/project/seed_data/teardrop.html",
                   "/home/vagrant/src/project/seed_data/triangle.html",
                   "/home/vagrant/src/project/seed_data/triangular.html",
                   "/home/vagrant/src/project/seed_data/unknown.html",
                   "/home/vagrant/src/project/seed_data/unspecified.html"]


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
            shape = row.contents[7].string
            duration = row.contents[9].string
            event_description = row.contents[11].string

            # date_time_raw:  u'3/11/16 19:30'
            # date_time is a datetime object.
            date_time_raw = row.contents[1].string
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