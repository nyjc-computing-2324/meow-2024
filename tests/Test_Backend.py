from unittest import *
from database import Account
import sqlite3
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

CURRENT TASKS/ISSUES:
- Continue with Student, CCA,etc testclasses
- UPDATE METHOD SEEMS WRONG
"""

class Test_Account(TestCase):

    def setUp(self):
        self.Account = Account(':memory:')
        self.name = '@aBc'
        self.password = 'Abcd1234'
        self.Account.insert(self.name,self.password)

    def test_insert(self):
        """
        Checks if the provided data is correctly inserted into
        the Account table with the insert method
        """
        self.assertTrue(self.Account.retrieve('username',self.name),'Insert function failed')
        self.result_insert = TextTestRunner().run(defaultTestLoader.loadTestsFromName("test_insert"))

    def test_update(self):
        """
        By Vincent & Hong Zhao
        Checks if a record is correctly updated in the Account
        table with the update method (maybe done)
        """
        if not self.result_insert.wasSuccessful():
            self.skipTest("Skipping test condition as insertion does not work")
            
        self.password = "aBCD1234"
        self.Account.update(1, 'password', self.password)
        with sqlite3.connect(self.Account.database_name) as conn:
            cursor = conn.cursor()
            query = """
                    SELECT *
                    FROM "Account"
                    WHERE "password" == ?;
                    """
            params = (self.password,)
            cursor.execute(query, params)
            record = cursor.fetchone()
            conn.commit()
        self.assertEqual(record[2], self.password, "Update method failed")

    def test_retrieve(self):
        """
        By Vincent & Hong Zhao
        Checks if a record is correctly retrieved from the
        Account table with the retrieve method (perhaps finished)
        """
        if not self.result_insert.wasSuccessful():
            self.skipTest("Skipping test condition as insertion does not work")
            
        self.assertEqual(self.name, self.Account.retrieve('username',self.name)[1], 'Retrieve method failed using username')      
        self.assertEqual(self.name, self.Account.retrieve('account_id','1')[1], 'Retrieve method failed using account_id')
        

    def test_delete(self):
        """
        By Vincent & Hong Zhao
        Checks if a record is correctly deleted from the Account
        table with the delete method, using both username and
        account_id, provided the insert method works
        """
        if not self.result_insert.wasSuccessful():
            self.skipTest("Skipping test condition as insertion does not work")
            
        del_target = self.Account.retrieve('username', self.name)
        self.Account.delete('username',del_target[0])
        self.assertIsNone(self.Account.retrieve('username', self.name), 'Delete method failed using username')
        
        self.Account.insert(self.name,self.password)
        self.Account.delete('account_id',del_target[0])
        self.assertIsNone(self.Account.retrieve('username', self.name), 'Delete method failed using account_id')
        
        
