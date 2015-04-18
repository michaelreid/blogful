
# import components of environment and python modules
import os
import unittest
import datetime

# import components of application
import blog
from blog.filters import *


# Configure my blog to use the testing configuration
if not "CONFIG PATH" in os.environ:
    os.environ["CONFIG_PATH"] = "blog.config.TestingConfig"



# UNIT TESTS to test the dateformat filter
class FilterTests(unittest.TestCase):

    def testDateFormat(self):
    # Test that date format works for turn of century
        date = datetime.date(1999, 12, 31)
        formatted = dateformat(date, "%y/%m/%d")
        self.assertEqual(formatted, "99/12/31")

    def testDateFormatNone(self):
    # Test that the formatter doesn't through an error if no date supplied
        formatted = dateformat(None, "%y/%m/%d")
        self.assertEqual(formatted, None)






if __name__ == "__main__":
    unittest.main()

