import json
from unittest import TestCase
from model import connect_to_db, db, Event, CityPop, example_data
from server import app, per_capita_info
import server
import unittest
from flask import jsonify


class FlaskTestsBasic(TestCase):
    """Flask tests."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

    def test_index(self):
        """Test homepage page."""

        result = self.client.get("/")
        self.assertIn("background: url(/static/img/ufo.gif)", result.data)

    def test_map_page(self):
        """Test map page."""

        result = self.client.get("/events")
        self.assertIn("<div id='map'>", result.data)
        self.assertIn("<input type='submit'", result.data)


class FlaskTestsDatabase(TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        example_data()

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

    def test_events_json(self):
        """Test /events.json page."""

        result = self.client.get("/events.json")
        self.assertIn("A hazey orange object", result.data)

    def test_population_json(self):
        """Test /population.json page."""

        result = self.client.get("/population.json")
        self.assertIn("Abbeville city", result.data)

    def test_per_capita_info(self):
        """Unit test"""

        # Test currently failing due to not enough example data (don't have
        # data for each state, therefore getting a ZeroDivisionError: float
        # division by zero)
        # Possibility: mock the data

        client = server.app.test_client()
        result = client.get('/reports-per-capita.json')
        assert isinstance(jsonified, dict)

    # Will look into writing this test after setting up FlaskMail.
    # def test_login(self):
    #     """Test login page."""

    #     result = self.client.post("/login",
    #                               data={"user_id": "rachel", "password": "123"},
    #                               follow_redirects=True)
    #     self.assertIn("You are a valued user", result.data)


# class FlaskTestsLoggedIn(TestCase):
#     """Flask tests with user logged in to session."""

#     def setUp(self):
#         """Stuff to do before every test."""

#         app.config['TESTING'] = True
#         app.config['SECRET_KEY'] = 'key'
#         self.client = app.test_client()

#         with self.client as c:
#             with c.session_transaction() as sess:
#                 sess['user_id'] = 1

#     def test_important_page(self):
#         """Test important page."""

#         result = self.client.get("/important")
#         self.assertIn("You are a valued user", result.data)


# class FlaskTestsLoggedOut(TestCase):
#     """Flask tests with user logged in to session."""

#     def setUp(self):
#         """Stuff to do before every test."""

#         app.config['TESTING'] = True
#         self.client = app.test_client()

#     def test_important_page(self):
#         """Test that user can't see important page when logged out."""

#         result = self.client.get("/important", follow_redirects=True)
#         self.assertNotIn("You are a valued user", result.data)
#         self.assertIn("You must be logged in", result.data)


if __name__ == "__main__":
    import unittest

    unittest.main()