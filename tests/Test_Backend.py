from unittest import *
from database import Account
import auth
import sqlite3
from dbfunctions import *
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
        self.account = get_account('qa')
        self.name = '@aBc'
        self.password = 'Abcd1234'
        self.password_hash, self.salt = auth.create_hash(self.password)
        self.account.insert(self.name, self.password_hash, self.salt)

    def test_insert(self):
        """
        Checks if the provided data is correctly inx de4serted into
        the Account table with the insert method, ie. if the name
        attribute of the retrieved record matches with the
        inserted record's name
        """

        with sqlite3.connect(self.account.database_name) as conn:
            cursor = conn.cursor()
            query = """
                    SELECT *
                    FROM "account"
                    WHERE "username" == ?;
                    """
            params = (self.name,)
            cursor.execute(query, params)
            record = cursor.fetchone()
            conn.commit()
        self.assertIsNotNone(record, 'Record was not inserted at all')
        self.assertEqual(record[2], self.password_hash, 'Password inserted wrongly')
        self.assertEqual(record[3], self.salt, 'Salt inserted wrongly')
        self.result_insert = TextTestRunner().run(defaultTestLoader.loadTestsFromName("test_insert"))

    def test_update(self):
        """
        By Vincent & Hong Zhao
        Checks if a record is correctly updated in the account
        table with the update method (maybe done)
        """
        if not self.result_insert.wasSuccessful():
            self.skipTest("Skipping test condition as insertion does not work")
            
        self.new_password = "aBCD1234"
        self.new_password_hash, _ = auth.create_hash(self.new_password)
        self.account.update(1, 'password', self.new_password_hash)
        with sqlite3.connect(self.account.database_name) as conn:
            cursor = conn.cursor()
            query = """
                    SELECT *
                    FROM "account"
                    WHERE "password" == ?;
                    """
            params = (self.new_password_hash,)
            cursor.execute(query, params)
            record = cursor.fetchone()
            conn.commit()
        self.assertIsNotNone(record, 'Record somehow got deleted during updating')
        self.assertEqual(record[2], self.new_password_hash, "Update method failed")

    def test_retrieve(self):
        """
        By Vincent & Hong Zhao
        Checks if a record is correctly retrieved from the
        account table with the retrieve method (perhaps finished)
        """
        if not self.result_insert.wasSuccessful():
            self.skipTest("Skipping test condition as insertion does not work")
            
        self.assertEqual(self.password_hash, self.account.retrieve('username',self.name)[2], 'Retrieve method failed using username')      
        self.assertEqual(self.password_hash, self.account.retrieve('account_id','1')[2], 'Retrieve method failed using account_id')
        

    def test_delete(self):
        """
        By Vincent & Hong Zhao
        Checks if a record is correctly deleted from the account
        table with the delete method, using both username and
        account_id, provided the insert method works
        """

        if not self.result_insert.wasSuccessful():
            self.skipTest("Skipping test condition as insertion does not work")
            
        del_target = self.account.retrieve('username', self.name)
        self.account.delete('username',del_target[0])
        self.assertIsNone(self.account.retrieve('username', self.name), 'Delete method failed using username')
        
        password, salt = auth.create_hash(self.password)
        self.account.insert(self.name,password,salt)
        self.account.delete('account_id',del_target[0])
        self.assertIsNone(self.account.retrieve('username', self.name), 'Delete method failed using account_id')


class Test_Student(TestCase):
    
    def setUp(self):
        self.student = get_student('qa')
        self.name = 'Racist_test'
        self._class = 4444
        self.email = 'racist@gmail.com'
        self.acc_id = 666
        self.student.insert(self.name, self._class, self.email, self.acc_id)
    
    def test_insert(self):
        """
        Docstring
        """
        with sqlite3.connect(self.student.database_name) as conn:
            cursor = conn.cursor()
            query = """
                    SELECT *
                    FROM "student"
                    WHERE "name" == ?;
                    """
            params = (self.name,)
            cursor.execute(query, params)
            record = cursor.fetchone()
            conn.commit()
        self.assertIsNotNone(record, 'Record was not inserted at all')
        self.assertEqual(record[2], self.class, 'Class inserted wrongly')
        self.assertEqual(record[3], self.email, 'E-mail inserted wrongly')
        self.assertEqual(record[4], self.acc_id, 'Account ID inserted wrongly')
        self.result_insert = TextTestRunner().run(defaultTestLoader.loadTestsFromName("test_insert"))
    
    def test_update(self):
        """
        Docstring
        """
        if not self.result_insert.wasSuccessful():
            self.skipTest("Skipping test condition as insertion does not work")
    
        self.fields = ["name", "class", "email", "account_id"]
        self.values = ["Racist Too", 6969, "ray2@gmail.com", 999]
        self.og = ['Racist_test', 4444, 'racist@gmail.com', 666]

        for x in range(len(self.fields)):
            self.student.update(1, self.fields[x], self.values[x])
            with sqlite3.connect(self.student.database_name) as conn:
                cursor = conn.cursor()
                query = f"""
                        SELECT *
                        FROM "student"
                        WHERE {self.fields[x]} == ?;
                        """
                params = (self.values[x],)
                cursor.execute(query, params)
                record = cursor.fetchone()
                conn.commit()
            self.assertIsNotNone(record, 'Record somehow got deleted during updating')
            self.assertEqual(record[1+x], self.values[x], f"Update method failed: Failed to update {self.fields[x]}")

            self.student.update(1, self.fields[x], self.og[x])
            
                
                
        
        
    
    def test_retrieve(self):
        """
        Docstring
        """
        if not self.result_insert.wasSuccessful():
            self.skipTest("Skipping test condition as insertion does not work")

        
        
        self.assertEqual(self.name, self.student.retrieve(1)[1], 'Could not retrieve name correctly.')      
        self.assertEqual(self._class, self.student.retrieve(1)[2], 'Could not retrieve class correctly.')
        self.assertEqual(self.email, self.student.retrieve(1)[3], 'Could not retrieve E-mail correctly.')
        self.assertEqual(self.acc_id, self.student.retrieve(1)[4], 'Could not retrieve Account ID correctly.')
    
    
    def test_delete(self):
        """
        Docstring
        """
    
        if not self.result_insert.wasSuccessful():
            self.skipTest("Skipping test condition as insertion does not work")

        self.student.delete(1)
        self.assertIsNone(self.student.retrieve(1), 'Delete method failed.')



