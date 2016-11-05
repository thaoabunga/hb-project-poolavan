"""Models and database functions for PoolaVan."""

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


#####################################################################
# Model definitions

class User(db.Model):
    """User of PoolaVan website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.String(10))
    smoking_preference = db.Column(db.String(15))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id=%s first_name=%s email=%s password=%s phone_number=%s gender=%s smoking_preference=%s>" % (self.user_id,
                                            self.first_name,
                                            self.email,
                                            self.password,
                                            self.phone_number,
                                            self.gender,
                                            self.smoking_preference)


class Trip(db.Model):
    """Initial trip details."""

    __tablename__ = "trips"

    trip_id = db.Column(db.Integer,
                         autoincrement=True,
                         primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    departure_address = db.Column(db.String(50), nullable=False)
    arrival_address = db.Column(db.String(50), nullable=False)
    trip_departure_at = db.Column(db.DateTime, nullable=False)
    trip_arrival_at = db.Column(db.DateTime, nullable=False)
    car_capacity = db.Column(db.Integer, nullable=False)
    activity = db.Column(db.Integer, db.ForeignKey("activities.activity_id", nullable=False)
    
    user = db.relationship('User', backref ='trips')

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Trip trip_id=%s departure_address=%s arrival_address=%s trip_departure_at=%s trip_arrival_at=%s car_capacity=%s activity=%s>" % (self.trip_id,
                                                 self.departure_address,
                                                 self.arrival_address,
                                                 self.trip_departure_at,
                                                 self.trip_arrival_at,
                                                 self.car_capacity,
                                                 self.activity,
                                                 trip_users)


class UserTrip(db.Model):
    """User and Trip details."""

    __tablename__ = "usertrips"

    user_trip_id = db.Column(db.Integer,
                          autoincrement=True,
                          primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    trip_id = db.Column(db.Integer, db.ForeignKey("trips.trip_id"), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.role_id"), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        s = "<UserTrip user_trip_id=%s user_id=%s trip_id=%s role=%s>"
        return s % (self.user_trip_id, self.user_id, self.trip_id,
                    self.role)

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

    recreation_acitivity = db.Column(db.String(40), nullable=False)

# class RideRequest(db.Model):
#     """User ride request."""

#     __tablename__ = "riderequests"

#     ride_request_id = db.Column(db.Integer,
#                           autoincrement=True,
#                           primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
#     active = db.Column(db.Boolean, nullable =False) #check to see if user is active, needs a ride
#     trip_departure_at = db.Column(db.DateTime, nullable=False)
#     trip_arrival_at = db.Column(db.DateTime, nullable=False)
#     activity = db.Column(db.String(60), nullable=False)

class TripMessage(db.Model): #second sprint TBD
    """Trip messages between users in a carpool."""

    __tablename__= "tripmessages"

    trip_message_id = db.Column(db.Integer,
                          autoincrement=True,
                          primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey("trips.trip_id"), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.role_id"), nullable=False)
    trip_message = db.Column(db.String(140), nullable=False)
    message_tracking = db.Column(db.DateTime)

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