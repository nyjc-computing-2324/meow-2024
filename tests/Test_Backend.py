from unittest import *
from database import Account
#IMPORTANT Please Read
"""
We will be using the unittest module instead to test frontend and backend.
Using this module follows a similar OOP structure to the classes we made last session 
One key difference is that you need to inherit from the 'unittest.TestCase' baseclass
Methods must also start with 'test' as below, else unittest can't recognise and run them

Read these guides to familiarise yourselves:

DataQuest Simple Guide: https://www.dataquest.io/blog/unit-tests-python/

unittest Documentation: https://docs.python.org/3/library/unittest.html


We will be starting with the Account class first, and move on to other ones.
"""

class Test_Account(TestCase):

    def setUp(self):
        self.Account = Account()
        self.name = '@aBc'
        self.password = 'Abcd1234'

    def test_insert(self):
        """
        Checks if the provided data is correctly inserted into
        the Account table with the insert method
        """
        self.Account.insert(self.name,self.password)
        assertTrue(self.Account.retrieve('username',self.name))

    def test_update(self):
        """
        By Vincent & Hong Zhao
        Checks if a record is correctly updated in the Account
        table with the update method (maybe done)
        """
        self.password = "aBCD1234"
        self.Account.update('password', self.password)
        assertEqual(self.account.retrieve('username', self.name)[2], self.password, "Update function failed")

    def test_retrieve(self):
        """
        By Vincent & Hong Zhao
        Checks if a record is correctly retrieved from the
        Account table with the retrieve method (perhaps finished)
        """
        assertEqual(self.name, self.account.retrieve('username',self.name), 'Retrieve function failed')

    def test_delete(self):
        """
        By Vincent & Hong Zhao
        Checks if a record is correctly deleted from the Account
        table with the delete method (possibly completed)
        """
        del_target = self.account.retrieve('username',self.name)
        self.account.delete(del_target[0])
        assertIsNone(del_target)
    