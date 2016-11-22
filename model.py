"""Models and database functions for PoolaVan."""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table
from datetime import datetime 


db = SQLAlchemy()

# dtDate = datetime.datetime.strptime(sDate, "%A, %d. %B %Y %I:%M%p")

#####################################################################
# Model definitions

class User(db.Model):
    """User of PoolaVan website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    username = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.String(10))
    smoking_preference = db.Column(db.String(15))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime)

    trips = db.relationship('Trip', secondary= 'usertrips', backref='users')


    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id=%s first_name=%s username=%s password=%s phone_number=%s gender=%s smoking_preference=%s>" % (self.user_id,
                                            self.first_name,
                                            self.username,
                                            self.password,
                                            self.phone_number,
                                            self.gender,
                                            self.smoking_preference)

    def serialize(self):
        return {
            'first_name': self.first_name,
            'username': self.username,
            'phone_number': self.phone_number,
            'gender': self.gender,
            'smoking_preference': self.smoking_preference
        }


class Trip(db.Model):
    """Initial trip details."""

    __tablename__ = "trips"

    trip_id = db.Column(db.Integer,
                         autoincrement=True,
                         primary_key=True)
    trip_name = db.Column(db.String(50), nullable=False)
    departure_address = db.Column(db.String(50), nullable=False)
    arrival_address = db.Column(db.String(50), nullable=False)
    trip_departure_at = db.Column(db.DateTime, nullable=False)
    trip_arrival_at = db.Column(db.DateTime, nullable=False)
    car_capacity = db.Column(db.Integer, nullable=False)
    # dtdeparture_at = datetime.datetime.strptime(sDate, "%A, %d. %B %Y %I:%M%p")
    # dtarrival_at = datetime.datetime.strptime(sDate, "%A, %d. %B %Y %I:%M%p")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Trip trip_id=%s trip_name=%s departure_address=%s arrival_address=%s trip_departure_at=%s trip_arrival_at=%s car_capacity=%s users=%s>" % (self.trip_id, self.trip_name,
                                                 self.departure_address,
                                                 self.arrival_address,
                                                 self.trip_departure_at,
                                                 self.trip_arrival_at,
                                                 self.car_capacity,
                                                 self.users)


class UserTrip(db.Model):
    """User and Trip details."""

    __tablename__ = "usertrips"

    user_trip_id = db.Column(db.Integer,
                          autoincrement=True,
                          primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    trip_id = db.Column(db.Integer, db.ForeignKey("trips.trip_id"), nullable=False)
    request = db.Column(db.String(50), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.role_id"), nullable=False)
    activity_id = db.Column(db.Integer, db.ForeignKey("activities.activity_id"), nullable=False)
    trip = db.relationship('Trip', uselist=False) #uselist this relationship is 1:1, single obj 
    usertrips_ = db.relationship('Activity', backref='usertrips')
    # write method on how to access user's role and 

    def __repr__(self):
        """Provide helpful representation when printed."""

        s = "<UserTrip user_trip_id=%s user_id=%s trip_id=%s request=%s role_id=%s, activity_id=%s>"
        return s % (self.user_trip_id, self.user_id, self.trip_id,
                    self.request, self.role_id, self.activity_id)



class Role(db.Model):
    """User roles in a carpool."""

    __tablename__ = "roles"

    role_id = db.Column(db.Integer,
                          autoincrement=True,
                          primary_key=True)
    role = db.Column(db.String(10), nullable=False)

class Activity(db.Model):
    """User activity match in a carpool."""

    __tablename__ = "activities"

    activity_id = db.Column(db.Integer,
                          autoincrement=True,
                          primary_key=True)

    recreation_type = db.Column(db.String(40), nullable=False)

    def serialize(self):
        return {
            'rec_type': self.recreation_type
        }

class RideRequest(db.Model):
    """RideRequest determines the passenger ride requests"""

    __tablename__ = "riderequests"

    OPTIONS = Choices(
        (1, "PENDING", _("Pending")),
        (2, "REJECTED", _("Rejected")),
        (3, "ACCEPTED", _("Accepted")),
    )

    # ride_request_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    # ride = db.Column(db.String(50),db.ForeignKey("UserTrip", related_name="request")
    # passenger = db.Column(db.String(50), db.ForeignKey("Role", )
    # status = db.Column.PositiveSmallIntegerField(_("Status"), choices=OPTIONS, default=OPTIONS.PENDING)


    def __unicode__(self):
        """string representation"""
        return "By %s for ride #%d - %s" % (self.passenger.username, self.ride.id, self.status)


# class TripMessage(db.Model): #second sprint TBD
#     """Trip messages between users in a carpool."""

#     __tablename__= "tripmessages"

#     trip_message_id = db.Column(db.Integer,
#                           autoincrement=True,
#                           primary_key=True)
#     trip_id = db.Column(db.Integer, db.ForeignKey("trips.trip_id"), nullable=False)
#     role_id = db.Column(db.Integer, db.ForeignKey("roles.role_id"), nullable=False)
#     trip_message = db.Column(db.String(140), nullable=False)
#     message_tracking = db.Column(db.DateTim

#####################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///poolavan'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will
    # leave you in a state of being able to work with the database
    # directly.

    from server import app

    connect_to_db(app)
    db.create_all()
    print "Connected to DB."