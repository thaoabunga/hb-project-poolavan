import unittest
import server
from jinja2 import StrictUndefined
from flask import Flask, render_template, request, redirect, session, flash, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from datetime import datetime
import json
from model import connect_to_db, db, User, Trip, UserTrip, Role, Activity

class MyAppUnitTestCase(TestCase):
    def setUp(self):
    """Stuff to do before every test."""
        self.client = app.test_client()
        app.config['TESTING'] = True

        connect_to_db(app, "postgresql:///testdb")

        db.create_all()
        example_data()

    def tearDown(self):
    """Do at end of every test."""
        db.session.close()
        db.drop_all()

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

    def test_mytrips(self):
        client = server.app.test_client()
        server.app.config['TESTING'] = True
        result = client.get('/mytrips')
        self.assertIn('<h2>My Trips:</h2>', result.data)


if __name__ == "__main__":
    unittest.main()