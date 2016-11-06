
from jinja2 import StrictUndefined

from flask import Flask, render_template, request, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension


from model import connect_to_db, db, User, Trip, Role, Activity

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


@app.route("/trips")
def trip_list():
    """Show list of trips."""

    trips = Trip.query.order_by(Trip.departure_address).all()
    return render_template("trip_list.html", 
                            trips=trips)


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
    print "entering the register new user method"

    first_name = request.form['first_name']
    username = request.form['username']
    password = request.form['password']
    phone_number = request.form['phone_number']
    gender = request.form['gender']
    smoking_preference = request.form['smoking_preference']

    print "write all variables from request"

    user_in_db = db.session.query(User).filter(User.username==username).all()

    print user_in_db

    # if username (email) is in not in database, add them 
    if not user_in_db:
        # add to db

        new_user = User(first_name=first_name, username=username, password=password, phone_number=phone_number, gender=gender, smoking_preference=smoking_preference)
        db.session.add(new_user)
        db.session.commit()

        print new_user

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

@app.route("/createtrip", methods=['GET']) #get will go into flask to id route and will call createtrip_form.html, a resource is being returned via the url
def createtrip_form():
    """Display new trips."""

    return render_template("createtrip_form.html") 

@app.route("/createtrip", methods=['POST']) 
def create_trip():
    """User creates a trip."""

    #create trip form in html
    #add current user to the trip
    username = session["user_id"]
    current_user = User.query.filter_by(user_id=username).first()
    #create a list of users in a trip


 





    

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug
    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host="0.0.0.0")