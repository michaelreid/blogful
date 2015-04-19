# Import OS, Environment & Python modules
import os
import unittest
import multiprocessing
import time
from urlparse import urlparse

# Import external modules
from werkzeug.security import generate_password_hash
from splinter import Browser

# Configure app to use test database
os.environ["CONFIG_PATH"] = "blog.config.TestingConfig"

# Import app's modules
from blog import app
from blog import models
from blog.database import Base, engine, session



# Set class to test views
class TestViews(unittest.TestCase):

    # Set up the TestCase
    def setUp(self):
        """ Test Setup """
        # Initiate an instance of the Phantom browser
        # [not a `test_client()` like integration test]
        #
        # A Splinter Browser using the Phantom Driver
        #
        self.browser = Browser("phantomjs")

        # Set up the database tables
        Base.metadata.create_all(engine)

        # Create an example user
        self.user = models.User(name="Alex", email="alex@gmail.com",
                                password=generate_password_hash("test"))

        session.add(self.user)
        session.commit()

        # Multi-processing: this handles setting up the server
        # [because visiting the app with a browser client].
        #
        # The running app takes a process, so need to start
        # the browser in separate process [concurrency].
        #
        self.process = multiprocessing.Process(target=app.run)
        # Start the server in separate process
        self.process.start()
        # Wait for 1 second while server starts
        time.sleep(1)

        
    # First test: try correct login information
    def testLoginCorrect(self):

        # First visit the login page
        self.browser.visit("http://0.0.0.0:8080/login")

        # Then fill out the login details
        # looks for an <input> element in HTML which has
        # `name` element matching first argument
        self.browser.fill("email", "alex@gmail.com")
        self.browser.fill("password", "test")

        # Click the login button
        button = self.browser.find_by_css("button[type=submit]")
        button.click()

        # Test login redirects to root directory correctly
        self.assertEqual(self.browser.url, "http://0.0.0.0:8080/")



    # Second test: try incorrect login information
    def testLoginIncorrect(self):

        # First visit the login page
        self.browser.visit("http://0.0.0.0/login")

        # Then fill out the login details
        self.browser.fill("email", "bill@email.com")
        self.browser.fill("password", "test")

        # Click the login button
        button = self.browser.find_by_css("button[type=submit]")
        button.click()

        # Test login redirects to root directory correctly
        self.assertEqual(self.browser.url, "http://0.0.0.0:8080/")


            
    # Finish the TestCase
    def tearDown(self):
        """ Test teardown """
        # Finish the server process
        self.process.terminate()

        # Finish use of the database
        session.close()

        # Finish with the database interface
        engine.dispose()

        # Drop all the database tables
        Base.metadata.drop_all(engine)

        # Close the browser
        self.browser.quit()


# Set up so can call test from Command Line
if __name__ == "__main__":
    unittest.main()