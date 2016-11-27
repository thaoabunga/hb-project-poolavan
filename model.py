"""Models and database functions for PoolaVan."""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table
from datetime import datetime 


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
            'user_id': self.user_id,
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
    trip = db.relationship('Trip', uselist=False) 
    usertrips_ = db.relationship('Activity', backref='usertrips')


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



#####################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///poolavan'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":

    from server import app

    connect_to_db(app)
    db.create_all()
    print "Connected to DB."