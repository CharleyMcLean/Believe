# Believe

Inspired by the National UFO Reporting Center Online Database, Believe was created to help people visualize where the most frequent UFO sightings are.  UFO reports and population data from the U.S. Census Bureau were used to create heat map layers for interesting data comparison.  Both heatmap layers may be toggled on and off, and there are buttons to toggle gradient color, radius, and opacity for each layer.  Users may also view charts representing the number of UFO reports per capita for each state, and the number of UFO reports for each day of the week.

##Contents
* [Tech Stack](#technologies)
* [Features](#features)
* [Installation](#install)
* [About Me](#aboutme)

## <a name="technologies"></a>Technologies
Tech Stack: PostgreSQL, SQLAlchemy, Python, Flask, JavaScript, HTML, CSS, JQuery, Beautiful Soup, Chart.js, Bootstrap.<br/>
APIs: Google Maps with visualization library, Geocoder<br/>

## <a name="features"></a>Features

Using a simple UI, users can choose to either be taken to a bar or restaurant:
![](https://cloud.githubusercontent.com/assets/18404713/18288887/059969d2-7432-11e6-9957-9dc41d04d753.png)

Users can then select their pricing and venue preferences:
![](https://cloud.githubusercontent.com/assets/18404713/18288891/05ac5092-7432-11e6-9efa-73d7d0ca365c.png)

They then enter their location:
![](https://cloud.githubusercontent.com/assets/18404713/18288890/05ab00ca-7432-11e6-82b9-e999ce98efc3.png)

Uber prompts them for authorization:
![](https://cloud.githubusercontent.com/assets/18404713/18288892/05afdb68-7432-11e6-8934-3874fad5d45d.png)
![](https://cloud.githubusercontent.com/assets/18404713/18292911/babcb71c-7444-11e6-9465-96add8353b97.png)

The request is then completed and users can view a "sneak preview" while they wait for their ride:
![](https://cloud.githubusercontent.com/assets/18404713/18288885/0597a5e8-7432-11e6-96fb-f5743f78792f.png)
![](https://cloud.githubusercontent.com/assets/18404713/18288889/059a2958-7432-11e6-8abd-0892678ecac5.png)

Users can also view their visit history:
![](https://cloud.githubusercontent.com/assets/18404713/18288886/05989da4-7432-11e6-98c7-4a2be7105e92.png)

The app also has a user management system incorporating password encryption.

## <a name="install"></a>Installation

To run Believe:

Install PostgreSQL (Mac OSX)

Clone or fork this repo:

```
https://github.com/CharleyMcLean/Believe.git
```

Create and activate a virtual environment inside your Believe directory:

```
virtualenv env
source env/bin/activate
```

Install the dependencies:

```
pip install -r requirements.txt
```

Set up the database:

```
python -i model.py
db.create_all()
quit()
psql ufo_reports < dump.sql
```

Run the app:

```
python server.py
```

You can now navigate to 'localhost:5000/' to access Believe.

## <a name="aboutme"></a>About Me
The developer lives in the San Francisco Bay Area. This is her first software project.