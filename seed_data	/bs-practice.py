from bs4 import BeautifulSoup
import lxml


def extract_data(filename):
    # Create the soup object.
    soup = BeautifulSoup(open(filename), "lxml")
    
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
        full_url = 'http://www.nuforc.org/webreports/' + end_of_url

        print date_time, city, state, shape, duration, event_description
        print full_url
