# Import the os and python modules
import os
import unittest
from urlparse import urlparse

# Import werkzeug module that deals with storing passwords
from werkzeug.security import generate_password_hash

# Configure app to use the test database
os.environ["CONFIG_PATH"] = "blog.config.TestingConfig" # string is path to TestConfig class

# Import the appication and it's models and database classes & methods
from blog import app
from blog import models
from blog.database import Base, engine, session


# INTEGRATION TESTING the applications views
class TestViews(unittest.TestCase):

    # Set up the testing of integration
    def setUp(self):
        """ Test setup """

        # Setting up a test_client enables calls to views
        # so that can see responses and test integrations
        self.client = app.test_client()

        # Test tables in test database
        Base.metadata.create_all(engine)

        # Create an example user
        self.user = models.User(name="Anthony", email="anthony@gmail.com",
                                password=generate_password_hash("test"))

        # Add example user to database
        session.add(self.user)
        session.commit()


    # not testLogin becuase method used in integration test below
    def simulate_login(self):   
        # simulate_login mimics all elements that Flask-Login looks for
        # when logging in a user
        with self.client.session_transaction() as http_session:
            http_session["user_id"] = str(self.user.id)
            http_session["_fresh"] = True

    
    def testAddPost(self):
        self.simulate_login()

        response = self.client.post("/post/add", data={
            "title": "Test Post",
            "post": "Test content"
        })

        # Is the response from add_post_post() 302 (successful)
        self.assertEqual(response.status_code, 302)
        # Is the redirect after post to the root /
        self.assertEqual(urlparse(response.location).path, "/")
        # Did the blog only post 1 post
        posts = session.query(models.Post).all()
        self.assertEqual(len(post), 1)

        # Is the post itself correct
        post = posts[0]
        # Is the title in the post the same as that input
        self.assertEqual(post.title, "Test Post")
        # Is the content the same as that input
        self.assertEqual(post.content, "<p>Test content</p>\n")
        # Is the author the same as that input
        self.assertEqual(post.author, self.user)
    

    # After tests complete, remove all data from database
    def tearDown(self):
        """ Test tear-down """
        session.close()

        # Remove the tables and their data from the database
        Base.metadata.drop_all(engine)

# Run test from command line
if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestViews)
    unittest.TextTestRunner(verbosity=3).run(suite)        

