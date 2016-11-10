
from jinja2 import StrictUndefined

from flask import Flask, render_template, request, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension


from model import connect_to_db, db, User, Trip, UserTrip, Role, Activity

app = Flask(__name__)

app.secret_key = "ABC"

app.jinja_env.undefined = StrictUndefined


@app.route('/')
def hello_world():
    """Homepage."""

    return render_template("homepage.html")


@app.before_request
def before_request():
    """ Default session["logged_in"] to false if next endpoint is not /login"""

    if "logged_in" not in session and request.endpoint != 'login':
        session["logged_in"] = False



################## Render Templates

@app.route("/users")
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("user_list.html", 
                            users=users)
@app.route("/users/<int:user_id>", methods=["GET"])
def user_detail(user_id):
    """Show info about user."""

    user = User.query.get(user_id)
    usertrip = user.trips
    #usertrip = User.trips
    #return render_template("user.html", user=user)
    return render_template("user.html", user=user, usertrip=usertrip)

# @app.route("/mytrips", methods=["GET"])
# def mytrips_detail():
#     """Show trips created by user."""

#     user_id = session["user_id"]

#     current_user = User.query.filter_by(user_id=user_id).first()



@app.route("/trips") #add another activity search route, form submits to trip activity
def trip_list():
    """Show list of trips."""

    trips = Trip.query.order_by(Trip.departure_address).all()
    return render_template("trip_list.html", 
                            trips=trips)

@app.route("/trips/<int:trip_id>", methods=["GET"])
def trip_detail(trip_id):
    """Show info about trip."""

    trip = Trip.query.get(trip_id)
    return render_template("trip.html", trip=trip)

# if car capacity not at max, request to join a trip?
# filter car capacity ? find a way to update car capacity as users are added, removed, and max cap is reached



@app.route("/register", methods=["GET"])
def register_form():
    """Register users."""

    return render_template("register_form.html") 


@app.route('/logout', methods=['POST'])
def logout():
    """User logout."""
    # remove the username from the session if it's there
    session['user_id'] = None
    session['logged_in'] = False

    flash("Successfully logged out!")
    return redirect("/")


@app.route("/register", methods=["POST"])
def register_new_user():
    """Add new users."""

    first_name = request.form['first_name']
    username = request.form['username']
    password = request.form['password']
    phone_number = request.form['phone_number']
    gender = request.form['gender']
    smoking_preference = request.form['smoking_preference']


    user_in_db = db.session.query(User).filter(User.username==username).all()


    # if username (email) is in not in database, add them 
    if not user_in_db:
        # add to db

        new_user = User(first_name=first_name, username=username, password=password, phone_number=phone_number, gender=gender, smoking_preference=smoking_preference)
        db.session.add(new_user)
        db.session.commit()


    # redirect to homepage
    return redirect("/")



@app.route("/login", methods=['POST'])
def user_login():
    """User login"""

    username = request.form['username']
    password = request.form['password']


    if "user_id" not in session:
        session["user_id"] = {}

    current_user = User.query.filter_by(username=username).first()

    # check login credentials against database, and route user accordingly
    if not current_user:
        # redirect to /register
        flash("No record found. Please register!")
        return redirect("/register")

    elif current_user and current_user.password == password:
        # store username in Flask session
        session["user_id"] = current_user.user_id
        session["logged_in"] = True
        flash("Successfully logged in!")
        return redirect("/")

    # if username in db and password belongs to same user, redirect to homepage 
    elif current_user.password != password:
        flash("Password does not match. Please try again.")
        return redirect("/")

# @app.route("/newtrips", methods=['GET']) #get will go into flask to id route and will call createtrip_form.html, a resource is being returned via the url
# def createtrip_form():
#     """Display new trips."""

#     return render_template("newtrip_form.html")

@app.route("/createtrip")
def createtrip_form():
    """Show User Create trip form."""
    return render_template("createtrip_form.html") 

@app.route("/createtrip", methods=['POST']) 
def create_trip():
    """User creates a trip."""

    #create trip form in html
    #add current user to the trip
   
    user_id = session["user_id"]

    current_user = User.query.filter_by(user_id=user_id).first()



    #collect all variables
    #add to session
    #current_user.
    trip_name = request.form['trip_name']
    departure_address = request.form['departure_address']
    arrival_address = request.form['arrival_address']
    trip_departure_at = request.form['trip_departure_at']
    trip_arrival_at = request.form['trip_arrival_at']
    car_capacity = request.form['car_capacity']


    new_trip = Trip(trip_name=trip_name, 
                    departure_address=departure_address, 
                    arrival_address=arrival_address, 
                    trip_departure_at=trip_departure_at, 
                    trip_arrival_at=trip_arrival_at, 
                    car_capacity=car_capacity)
    db.session.add(new_trip)
    db.session.flush() #gives new_trip an id in order to complete the transaction not permanent- easy access

    new_user_trip = UserTrip(user_id=current_user.user_id, trip_id=new_trip.trip_id, request='active')

    db.session.add_all([new_trip, new_user_trip, current_user])

    db.session.commit()


    return redirect("/usertrip") # TODO: redirect to users within the same loc and activity (list of matching ride requests)

# @app.route("/usertrip")
# def usertrip_all():
#     """Show users within the same location and activity."""

#     user = User.query.get(user_id)
#     usertrip = user.trips.departure_address
#     #usertrip = User.trips
#     #return render_template("user.html", user=user)
#     return render_template("usertrip_list.html", user=user, usertrip=usertrip)

# @app.route("/usertrip/" + user_trip_id)
# def usertrip_all():
#     """Show usertrips details."""

#     UserTrip = UserTrip.query.get(user_trip_id)
#     return render_template("trip.html", trip=trip)

@app.route("/jointrip", methods=['POST'])
def join_trip():
    """User joins a trip."""

    current_user = User.query.filter_by(user_id=session['user_id']).first()
    trip_id = request.form['trip_id']
    trip = Trip.query.filter_by(trip_id=trip_id).first()

    new_user_trip = UserTrip(user_id=current_user.user_id, trip_id=trip.trip_id, request='active')

    db.session.add_all([new_user_trip, current_user])

    db.session.commit()  
    #return redirect("/trips/" + trip_id) # use url_for instead should this go to a wait for confirmation page?
    return redirect("/requestconfirmation")

@app.route("/requestconfirmation")
def confirmation_form():
    """User receives confirmation of joining a trip."""

    return render_template("request_confirmation.html")
    

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True
    app.config['DEBUG'] = True
    app.jinja_env.auto_reload = app.debug
    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host="0.0.0.0")