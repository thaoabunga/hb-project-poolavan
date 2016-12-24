# Poolavan

Poolavan is ridesharing flask application that brings adventurers into the great outdoors. It solves the problem of planning for a long-distance carpool into the wilderness, while reducing costs and environmental impact. Users can create trips, search for other users with common activity interests, and join existing trips. Poolavan connects people to opt outside. 


![POOLAVAN GIF](http://g.recordit.co/sIHbA67Nj7.gif)

# Table of Contents
* [Tech stack](#technologies)
* [Installation](#install)
* [Version 2.0](#future)

## <a name="technologies"></a>Technologies
Backend: Python, Flask
Frontend: JavaScript, jQuery, AJAX, Jinja2, Bootstrap, HTML/CSS
Database: PostgreSQL, SQLAlchemy
API: Google Maps API


## <a name="install"></a>Installation


####Prerequisites

- Install PostgreSQL (Mac OSX).
- Python 2.6 or greater.
- A Google account with Google Maps API enablement.


Clone repository:
```
$ git clone https://github.com/thaoabunga/hb-project-poolavan
```

Create a virtual environment:

```
$ virtualenv env
```
Activate the virtual environment.
```
$ source env/bin/activate
```
Install dependencies.
```
$ pip install -r requirements.txt
```
To enable the Google Maps API, create your project in the [Google Developers Console](https://developers.google.com/maps/documentation/javascript/).

Run PostgreSQL 

Create database with the name 'poolavan'.
```
$ createdb poolavan

$ psql poolavan
```
To run the app from the command line of the terminal, run
```
$ python server.py
```
If you want to use SQLAlchemy to query the database, run in interactive mode
```
$ python -i server.py
```

## <a name="future"></a>Version 2.0

Further development includes:
- [ ] User Profile Edit Functionality
- [ ] Database Migrations
- [ ] Text notifications via twilio API
