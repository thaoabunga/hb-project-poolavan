
from jinja2 import StrictUndefined
from flask import Flask, render_template, request, redirect, session, flash, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from datetime import datetime
import json
from model import connect_to_db, db, User, Trip, UserTrip, Role, Activity

app = Flask(__name__)

app.secret_key = "ABC"

app.jinja_env.undefined = StrictUndefined

################## Render Templates

@app.route('/')
def hello_world():
    """Homepage."""

    return render_template("homepage.html")

@app.route("/register", methods=["GET"])
def register_form():
    """Register users."""

    return render_template("register_form.html") 


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

    if not user_in_db:
        new_user = User(first_name=first_name, username=username, password=password, phone_number=phone_number, gender=gender, smoking_preference=smoking_preference)
        db.session.add(new_user)
        db.session.commit()

    return redirect("/")




@app.route('/userlogin', methods=['GET'])
def user_login():

    return render_template("userlogin.html")


# @app.route('/status.js', methods=['GET'])
# def user_status_login():

#     return render_template("status.js")

@app.route("/login", methods=['POST'])
def login():
    """User login"""

    username = request.form.get('username')
    password = request.form.get('password')
    
    if "user_id" not in session:
        session["user_id"] = {}

    current_user = User.query.filter_by(username=username).first()

    if not current_user:

        flash("No user found. Please register!")
        return redirect("/register")

    elif current_user and current_user.password == password:

        session["user_id"] = current_user.user_id
        session['username'] = current_user.first_name
        session["logged_in"] = True
        flash("Successfully logged in!")

        return redirect("/userhome")

    elif current_user.password != password:
        flash("Password does not match. Please try again.")

        return redirect("/")



@app.route('/logout', methods=['GET','POST'])
def logout():
    """User logout."""

    session['user_id'] = None
    session['logged_in'] = False

    return redirect("/")


@app.route('/userhome', methods=['GET', 'POST'])
def userhome():
    """User Homepage."""
    activities = Activity.query.all()
    return render_template("userhome.html", activities=activities)

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
    return render_template("user.html", user=user, usertrip=usertrip)

@app.route("/mytrips") 
def mytrips_detail():
    """Show trips created by user."""

    user_id = session["user_id"]
    user = User.query.get(user_id)
    passenger_role = Role.query.filter_by(role='Passenger').first()
    driver_role = Role.query.filter_by(role='Driver').first()

    my_user_trips = UserTrip.query.filter_by(user_id=user.user_id, role_id=driver_role.role_id)
    my_trip_ids = [user_trip.trip.trip_id for user_trip in my_user_trips.all()]
    user_trip_requests = UserTrip.query.filter(UserTrip.trip_id.in_(my_trip_ids), UserTrip.role_id==passenger_role.role_id)

   
    active_trips = my_user_trips.filter_by(request='active').all()
    pending_trips = user_trip_requests.filter_by(request='pending').all()
    rejected_trips = user_trip_requests.filter_by(request='rejected').all()

    user_rides = UserTrip.query.filter_by(user_id=user.user_id, role_id=passenger_role.role_id).all()
    
    return render_template(
        "mytrips.html",
        user=user,
        active_trips=active_trips,
        pending_trips=pending_trips,
        rejected_trips=rejected_trips,
        user_rides=user_rides,
    )

@app.route("/mytrips/<int:trip_id>",methods=['GET'])
def my_tripsdetail(trip_id):
    """Show trip details for user."""

    trip = Trip.query.get(trip_id)

    return render_template("mytripsdetail.html", trip=trip)


@app.route("/update_status/<int:trip_id>", methods=['POST'])
def update_status(trip_id):
    """Accept/Reject a user trip."""

    user_trip = UserTrip.query.get(trip_id)
    action = request.json['action']
    print action

    if (action == 'accept'):
        user_trip.request = 'active'
    elif (action == 'reject'):
        user_trip.request = 'rejected'

    db.session.add(user_trip)
    db.session.commit()
    return jsonify({ 'status': 'success' })


@app.route("/trips")
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


@app.route("/usertrip", methods=["GET"])
def activities_form():
    """Displays users' activities."""

    activity_id = request.args.get('activity_id')
    activities = UserTrip.query.filter_by(activity_id=activity_id).all() 
    rec_type = Activity.query.get(activity_id)

    users = set()
    for activity in activities:
        user = User.query.get(activity.user_id)
        users.add(user)

    return jsonify(users=[user.serialize() for user in users], rec_type=rec_type.serialize())

@app.route("/createtrip", methods=['GET', 'POST']) 
def create_trip():
    """User creates a trip."""


    if request.method == 'GET':
        activities = Activity.query.all()
        roles = Role.query.all()
        return render_template(
            "createtrip_form.html",
             activities=activities,
             roles=roles
        )

    else: 

        user_id = session["user_id"]
        current_user = User.query.filter_by(user_id=user_id).first()
        trip_name = request.form['trip_name']
        departure_address = request.form['departure_address']
        arrival_address = request.form['arrival_address']
        trip_departure_at = request.form['trip_departure_at']
        trip_arrival_at = request.form['trip_arrival_at']
        car_capacity = request.form['car_capacity']
        activity_id = request.form['recreation_activity']
        role_id = request.form['role_id']


        new_trip = Trip(trip_name=trip_name, 
                        departure_address=departure_address, 
                        arrival_address=arrival_address, 
                        trip_departure_at=trip_departure_at, 
                        trip_arrival_at=trip_arrival_at, 
                        car_capacity=car_capacity)


        db.session.add(new_trip)
        db.session.flush() 

        new_user_trip = UserTrip(
            user_id=current_user.user_id,
            trip_id=new_trip.trip_id,
            role_id=role_id, 
            activity_id=activity_id,
            request='active'
        )

        db.session.add_all([new_trip, new_user_trip, current_user])

        db.session.commit()


        return redirect("/userhome") 


@app.route("/jointrip", methods=['POST'])
def join_trip():
    """User joins a trip."""

    current_user = User.query.filter_by(user_id=session['user_id']).first()
    trip_id = request.form['trip_id']
    trip = Trip.query.filter_by(trip_id=trip_id).first()
    user_trip = UserTrip.query.filter_by(trip_id=trip.trip_id).first()
    passenger_role = Role.query.filter_by(role='Passenger').first()

    new_user_trip = UserTrip(
        user_id=current_user.user_id,
        trip_id=trip.trip_id,
        role_id=passenger_role.role_id, 
        activity_id=user_trip.activity_id,
        request='pending'
    )

    db.session.add_all([new_user_trip, current_user])

    db.session.commit()  

    return redirect("/requestconfirmation")

@app.route("/requestconfirmation")
def confirmation_form():
    """User receives confirmation of joining a trip."""

    return render_template("request_confirmation.html")
    

if __name__ == "__main__":

    app.debug = True
    app.config['DEBUG'] = True

    app.jinja_env.auto_reload = app.debug
    connect_to_db(app)

    app.run(port=5000, host="0.0.0.0")