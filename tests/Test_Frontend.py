from unittest import *
#IMPORTANT Please Read
"""
We will be using the unittest module instead to test frontend and backend.
Using this module follows a similar OOP structure to the classes we made last session 
One key difference is that you need to inherit from the 'unittest.TestCase' baseclass
Methods must also start with 'test' as below, else unittest can't recognise and run them

Read these guides to familiarise yourselves:

DataQuest Simple Guide: https://www.dataquest.io/blog/unit-tests-python/

unittest Documentation: https://docs.python.org/3/library/unittest.html

We'll start with this once Validate and some Backend classes like Account are done.
This is that it's easier for y'all to familiarise with the new module first 
"""


class Test_Frontend(TestCase):

    def setUp(self):
        pass

    def test_index(self):
        raise NotImplementedError

    def test_temp(self):
        raise NotImplementedError

    def test_home(self):
        raise NotImplementedError

    def test_about(self):
        raise NotImplementedError

    def test_login(self):
        raise NotImplementedError

    def test_register(self):
        raise NotImplementedError