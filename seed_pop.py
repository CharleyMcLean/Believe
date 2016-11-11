import csv

import geocoder

from model import CityPop, connect_to_db, db
from server import app


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


def load_city_populations():
    """Load population data from census csv file into database"""

    # Open the csv file and create a reader object; convert to list for iteration.
    populationFile = open("/home/vagrant/src/project/seed_data/population.csv")
    populationReader = csv.reader(populationFile)
    populationData = list(populationReader)

    total_added = 0

    for row in populationData:
        # Only gathering information for the geographic summary areas
        # coresponding to the code '162'.  This means 'incorporated place'
        # (cities that will successfully geocode!)
        if row[0] == '162':
            # Row indices obtained from census documentation.
            # Population data is based on the 2010 census.
            city = row[8]
            state = row[9]

            if type(row[10]) is int:
                population = row[10]
            else:
                population = row[11]
            lat_lng = get_lat_lng(city, state)
                # If lat_lng exists, capture the values of latitude and longitude.
            if lat_lng:
                # Unpack the list.
                latitude, longitude = lat_lng
            # If lat_lng is None, then geocoding did not return a result.
            else:
                print "tried geocoding, failed"
                continue

            print city, state

            city_pop = CityPop(city=city,
                               state=state,
                               population=population,
                               latitude=latitude,
                               longitude=longitude)

            db.session.add(city_pop)
            db.session.commit()
            total_added += 1

    print "total_added:", total_added


#######################################################################

if __name__ == "__main__":
    connect_to_db(app)
    # db.create_all()

    load_city_populations()
