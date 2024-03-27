from unittest import *
from database import Account
from validate import *
#IMPORTANT Please Read
"""
We will be using the unittest module instead to test frontend and backend.
Using this module follows a similar OOP structure to the classes we made last session 
One key difference is that you need to inherit from the 'unittest.TestCase' baseclass
Methods must also start with 'test' as below, else unittest can't recognise and run them

Read these guides to familiarise yourselves:

DataQuest Simple Guide: https://www.dataquest.io/blog/unit-tests-python/

unittest Documentation: https://docs.python.org/3/library/unittest.html
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

    


class Test_Account(TestCase):

    def setUp(self):
        self.Account = Account()
        self.name = '@aBc'
        self.password = 'Abcd1234'

    def test_insert(self):
        """
        By Vincent & Hong Zhao
        Checks if the provided data is correctly inserted into
        the Account table with the insert method
        """
        self.Account.insert(self.name,self.password)
        assertTrue(self.Account.retrieve('username',self.name))

    def test_update(self):
        """
        By Vincent & Hong Zhao
        Checks if a record is correctly updated in the Account
        table with the update method
        """
        raise NotImplementedError

    def test_retrieve(self):
        """
        By Vincent & Hong Zhao
        Checks if a record is correctly retrieved from the
        Account table with the retrieve method
        """
        raise NotImplementedError

    def test_delete(self):
        """
        By Vincent & Hong Zhao
        Checks if a resord is correctly deleted from the Account
        table with the delete method
        """
        raise NotImplementedError


class Test_Validate(TestCase):

    def set_up(self):
        """
        Sample username/password values for testing, you guys
        can add more values to test more cases
        """
        self.validname = '@aBc'
        self.invalidname = 'ABCD二十八'
        self.validpassword = 'Abcd1234'
        self.invalidpassword_notupperlowernumber = 'abcdsf'
        self.invalidpassword_notascii = 'ABCd二十八28'

    def test_username_isvalid(self):
        """
        Tests the username_isvalid method on validate.py
        """
        assertTrue(username_isvalid(self.validname),'Username should be valid')
        assertFalse(username_isvalid(self.invalidname),'Username should be invalid')

    def test_password_isvalid(self):
        """
        By Si Bin
        Tests the password_isvalid method on validate.py
        """
        raise NotImplementedError

    def test_user_isvalid(self):
        """
        By Si Bin
        Tests the user_isvalid method on validate.py
        """
        raise NotImplementedError