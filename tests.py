import unittest
import server
from jinja2 import StrictUndefined
from flask import Flask, render_template, request, redirect, session, flash, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from datetime import datetime
import json
from model import connect_to_db, db, User, Trip, UserTrip, Role, Activity



class MyAppUnitTestCase(unittest.TestCase):
    def setUp(self):
    # """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

        connect_to_db(app, "postgresql:///testdb")

        db.create_all()
        example_data()

    def tearDown(self):
        """Do at end of every test."""
        db.session.close()
        db.drop_all()

    def example_data():
        """Create some sample data."""

        SaffyTrip = Trip(trip_id=2, departure_address='Oakland', car_capacity=2)
        AnnaTrip = Trip(trip_id=11, departure_address='Berkeley', car_capacity=2)
        SamTrip = Trip(trip_id=6, departure_address='Oakland', car_capacity=3)

        Saffy = User(first_name='Saffy', )
        Anna = User(first_name='Anna', )
        Sam = User(name='Sam',)
       

        db.session.add_all([ SaffyTrip, AnnaTrip, SamTrip, Saffy, Anna, Sam])
        db.session.commit()


class MyAppIntegrationTestCase(unittest.TestCase):
    def test_index(self):
        client = server.app.test_client()
        result = client.get('/')
        self.assertIn('<title>Poolavan | Ridesharing for Adventurers. </title>', result.data)

    def test_userlogin(self):
        client = server.app.test_client()
        server.app.config['TESTING'] = True
        result = client.get('/userlogin', data ={'username': 'password'})
        self.assertIn('<div id="homepage-block"></div>', result.data)

    def test_register(self):
        client = server.app.test_client()
        server.app.config['TESTING'] = True
        result = client.get('/register')
        self.assertIn('<h1>Register</h1>', result.data)

    def test_register_new_user(self): # TODO: Review all coverage
        client 

    def test_mytrips(self):
        client = server.app.test_client()
        server.app.config['TESTING'] = True
        result = client.get('/mytrips')
        self.assertIn('<h2>Rejected requests:</h2>', result.data)



class FlaskTests(unittest.TestCase):

    def setUp(self):
    # """Stuff to do before every test."""

        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key'
        self.client = app.test_client()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1


if __name__ == "__main__":
    unittest.main()