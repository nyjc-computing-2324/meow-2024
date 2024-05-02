from typing import Optional
from dbfunctions import *
from database import init_tables
from unittest import *
from auth import create_hash

#Instantiating table objects
# student_profile = get_student('qa')
# test_cca = get_cca('qa')
# test_activity = get_activity('qa')

init_tables(conn_factory('qa', ':memory:'))

class Test_Account(TestCase):
    def setUp(self):
        # Set up connection to an in-memory SQLite database(jic)
        self.account = get_account('qa')
        self.connection = sqlite3.connect(':memory:')
        self.cursor = self.connection.cursor()

        # Create the 'Account' table using direct SQL query
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS "account" (
        "account_id" INTEGER PRIMARY KEY,
        "username" TEXT NOT NULL UNIQUE,
        "password" TEXT NOT NULL,
        "salt" BYTES NOT NULL
        );
        ''')
        self.connection.commit()
    
    def test_create_account(self): #Account object taken in just in case for future testing
        """
        Test checks whether the create_account function works.
        
        As of late, it does not due to the insert method of account
        misbehaving with our in-memory testing database, hence we
        cannot directly call the create_account function
        Hence, we are testing its record insertion logic manually via
        
        1. Manual sql INSERT query
        2. Account object's insert method
        """

        #Test Case
        username1 = 'name1'
        password1 = 'Password1'
        username2 = 'name2'
        password2 = 'Password2'

        #Check for presence of account table
        query = """
            SELECT name
            FROM sqlite_master
            WHERE  type='table' 
            AND name = ?;
            """
        params = ('account',)
        self.cursor.execute(query,params)
        tables = self.cursor.fetchall()
        self.assertNotEqual(tables, [], msg="No 'account' table created in database")

        #Function identifies error msg for specific case and asserts
        def check_for_record(username: str) -> None:

            result = retrieve_account(username)

            #Get all records in account table
            self.cursor.execute('SELECT * from Account')

            #Assertions
            self.assertTrue(isinstance(result,dict))
            self.assertIsNotNone(result,f"Record not inserted at all, result = {result}")
            self.assertEqual(result['username'], username, f"Record inserted incorrectly, result={result}")

        #Insert Record via manual sql query
        create_account(username1, password1)

        #Check the record inserted via manual sql query
        check_for_record(username1)        


    

    def tearDown(self):
        self.connection.close()
        
        
        

def login():
    pass


class Test_Profile(TestCase):
    def setUp(self):
        self.profile = get_student()
        self.name1 = 'abcdefghi!'
        self._class1 = '2328'
        self.email1 = 'name@gmail.com'
        self.name2 = 'qwertyuiop'
        self._class2 = '2401'
        self.number = 12345678
        self.about = "I would punt a baby like a rugby ball if it was crying too loud"
        self.username = "ABABAB"
        self.conn = self.profile.get_conn()
        self.cursor = conn.cursor()
        create_profile(self.name1, self._class1, self.email1, self.number, self.about, self.username)
        
    def test_create_profile(self):
        #Check for presence of student table
        query = """
            SELECT name
            FROM sqlite_master
            WHERE  type = 'table' 
            AND name = ?;
            """
        params = ('student',)
        self.cursor.execute(query,params)
        tables = self.cursor.fetchall()
        self.assertNotEqual(tables, [], msg="No 'student' table created in database")
        data = retrieve_profile(self.username)
        self.assertEqual(type(data), dict, "Retrieve does not return dictionary")
        self.assertEqual(data['username'], self.username, "Create function failed")
        
        
    def test_update_profile(self):
        record = retrieve_profile(self.username)
        upd = [self.name2, self._class2]
        for param in upd:
            update_profile(self.username, upd)
        record1 = retrieve_profile(self.username)
        self.assertEqual(type(record), dict, "Retrieve does not return dictionary")
        self.assertNotEqual(record["name"], record1["name"], "Update function failed, name update unsuccessful")
        self.assertNotEqual(record["class"], record1["class"], "Update function failed, class update unsuccessful")

    def test_retrieve_profile(self):
        record = retrieve_profile(self.username)
        self.assertEqual(type(record), dict, "Retrieve does not return a dictionary")
        self.assertEqual(record["class"], self.class1, "Retrieved incorrect information")

    def test_delete_profile(self):
        delete_profile(self.username)
        try:
            result = retrieve_profile(self.username)
            self.assertNotEqual(type(result),dict, "Delete function failed")
        except AttributeError:
            self.assertEqual(1,1,"idk how this one even fails but good job if it does i guess")
        
        
    
    def tearDown(self) -> None:
        self.conn.close()