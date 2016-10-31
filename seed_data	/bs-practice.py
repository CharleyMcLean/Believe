from bs4 import BeautifulSoup
import lxml

# Gathering data from shape 'changed'.
soup_changed = BeautifulSoup(open("shape-changed.html"), "lxml")

time_of_event = soup_changed.tbody.tr.contents[1].string
city = soup_changed.tbody.tr.contents[3].string
state = soup_changed.tbody.tr.contents[5].string
shape = soup_changed.tbody.tr.contents[7].string
duration = soup_changed.tbody.tr.contents[9].string
event_description = soup_changed.tbody.tr.contents[11].string

shape_changed_events = {"Time of event": time_of_event,
                        "City": city,
                        "State": state,
                        "Shape": shape,
                        "Duration of event": duration,
                        "Description of event": event_description}


# Gathering data from shape 'crescent'
soup_crescent = BeautifulSoup(open("shape-crescent.html"), "lxml")

# soup_crescent.tbody.contents is a list, with new lines at even indices,
# and table rows with data at odd indices.
# This is a list of html strings, corresponding to the rows of data.
crescent_rows = soup_crescent.tbody.contents[1::2]


def extract_data(shape_rows):
    for row in shape_rows:
        # For each row of html, extract the event details.
        time_of_event = row.contents[1].string
        city = row.contents[3].string
        state = row.contents[5].string
        shape = row.contents[7].string
        duration = row.contents[9].string
        event_description = row.contents[11].string

        # Create a dictionary for each event with its details.
        event_details = {"Time of event": time_of_event,
                         "City": city,
                         "State": state,
                         "Shape": shape,
                         "Duration of event": duration,
                         "Description of event": event_description}

        # Create an empty list to hold the event dictionaries.
        all_events = []

        # Append each event details dictionary to the all_events list.
        all_events.append(event_details)

    return all_events