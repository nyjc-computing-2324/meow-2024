from typing import Optional
from unittest.case import _AssertRaisesContext
import sqlite3
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
        self.conn = sqlite3.connect(':memory:')
        self.cursor = self.conn.cursor()

    # Create the 'account' table using direct SQL query
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS "account" (
            "activity_id" INTEGER PRIMARY KEY,
            "name" TEXT NOT NULL UNIQUE,
            "date" TEXT NOT NULL, 
            "location" TEXT NOT NULL,
            "organiser_id" INTEGER,
            FOREIGN KEY ("organiser_id") REFERENCES account("student_id")
        );
        ''')
        self.conn.commit()

        #initialise tables
        init_tables(conn_factory('qa', ':memory:'))

    def test_table(self):
        """
        Test checks for presence of account table
        """
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
    
    def test_create_account(self):
        """
        Test checks whether the create_account function
        works.
        """

        #Test Case
        username = 'name1'
        password = 'Password1'

        #Insert Record via manual sql query
        create_account(username, password)

        result = retrieve_account(username)

        #Assertions
        self.assertTrue(isinstance(result,dict))
        self.assertIsNotNone(result,f"Record not inserted at all, result = {result}")
        self.assertEqual(result['username'], username, f"Record inserted incorrectly, result={result}")


    def test_login(self):
        """
        Tests the login() function in dbfunctions.py.
        
        This test assumes that create_account() works.
        """
        #Test username and password
        right_username_login = 'rightnamelogin'
        right_password_login = 'RightPa55wordl0gin'

        #Test non-existent username and password
        wrong_username_login = 'wrongnamelogin'
        wrong_password_login = 'WrongPa55wordl0gin'

        #Create test account
        create_account(right_username_login, right_password_login)

        #Test successful login
        self.assertTrue(login(right_username_login, right_password_login), 'Login should work.')

        #Test unsuccessful login
        self.assertFalse(login(right_username_login, wrong_password_login), 'Login should not work: Wrong password.')
        self.assertFalse(login(wrong_username_login, right_password_login), 'Login should not work: Wrong username.')
        self.assertFalse(login(wrong_username_login, wrong_password_login), 'Login should not work: Wrong username and password.')


    def test_username_taken(self):
        """
        Tests the username_taken() function in dbfunctions.py.
        
        This test assumes that create_account() works.
        """
        #Test username and password
        taken_username = 'alreadytakenname'
        password_of_taken_username = 'P4ssword0fTakenName'

        #Test non-existent username
        not_taken_username = 'notyettakenname'

        #Create the "existing account"
        create_account(taken_username, password_of_taken_username)

        #Test if username_taken function
        self.assertTrue(username_taken(taken_username), 'Username should already be taken.')
        self.assertFalse(username_taken(not_taken_username), 'Username is not taken.')

    
    def test_retrieve(self):
        """
        Tests the retrieve_account() function in dbfunctions.py.
        
        This test assumes that create_account() works.
        """
        #Test username and password
        username_retrieve = 'usernameretrieve'
        password_retrieve = 'P4ssw0rdRetrieve'

        #Wrong username
        wrong_username_retrieve = 'wrongretrieve'

        #Create test account and retrieve data from account
        create_account(username_retrieve, password_retrieve)
        retrieved_data = retrieve_account(username_retrieve)

        #Test if data retrieved is correct
        self.assertEqual(retrieved_data['username'], username_retrieve, 'Username retrieved is wrong.')
        
        #Test if retrieving with non-existent account raises an error
        self.assertRaises(AttributeError, retrieve_account, wrong_username_retrieve)


    def test_delete_account(self):
        """
        Tests the delete_account() function in dbfunctions.py.
        
        This test assumes that create_account() and retrieve_account() works.
        """
        #Test username and password
        username = 'tobedeleted'
        password = '2Bdeleted'

        #Creat test account
        create_account(username, password)

        #Delete and test if account still exists
        delete_account(username)
        self.assertRaises(AttributeError, retrieve_account, username)

        
    def test_update_account(self):
        """
        Tests the update_account() function in dbfunctions.py.

        This test assumes that create_account(), retrieve_account(), and delete_account() works.
        """
        #Test set up
        old_username = 'oldusername'
        old_password = 'OldP4ssw0rd'

        new_username = 'newusername'
        new_password = 'NewP4ssw0rd'

        #Case 1: Change Password
        create_account(old_username, old_password)
        update_account(old_username, 'password', new_password )
        self.assertEqual(retrieve_account(old_username)['password'], new_password, 'Password update failed.')

        #Reset for Case 2
        delete_account(old_username)
        
        #Case 2: Change Username
        create_account(old_username, old_password)
        update_account(old_username, 'username', new_username)
        self.assertEqual(retrieve_account(new_username)['username'], new_username, 'Username update failed.')
        



    def tearDown(self):
        self.conn.close()
        
        
        




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


class Test_CCA(TestCase):
    def setUp(self):
        """
        Runs before every test
        """
        #Set up connection to an in-memory SQLite database too for ensuring table creation
        self.cca = get_cca('qa')
        self.conn = sqlite3.connect(':memory:')
        self.cursor = self.conn.cursor()
        self.name = 'NYRCS'
        self.type = 'clubs and societies'

        # Create the 'cca' table using direct SQL query
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS "cca" (
            "cca_id" INTEGER PRIMARY KEY,
            "name" TEXT NOT NULL UNIQUE,
            "type" TEXT NOT NULL 
        );
        ''')
        self.conn.commit()

        #initialise tables
        init_tables(conn_factory('qa', ':memory:'))

    def test_table(self):
        """
        Test checks for presence of cca table
        """
        query = """
            SELECT name
            FROM sqlite_master
            WHERE  type='table' 
            AND name = ?;
            """
        params = ('cca',)
        self.cursor.execute(query,params)
        tables = self.cursor.fetchall()
        self.assertNotEqual(tables, [], msg="No 'cca' table created in database")
    
    def test_create_cca(self):
        """
        Test checks whether the create_cca function works.
        """
        create_cca(self.name, self.type)
        result = retrieve_cca(self.name)
        #Assertions
        self.assertTrue(isinstance(result,dict), "Record retrieved is not a dict")
        self.assertIsNotNone(result,"Record not inserted at all")
        self.assertEqual(result['name'], self.name, f"Record inserted incorrectly, result={result}")

    def test_update_cca(self):
        """
        Test checks whether the update_cca function works
        """
        try:
            create_cca(self.name, self.type)
        except AttributeError:
            pass
            
        update_cca(self.name,'name','Biz Club')

        result = retrieve_cca('Biz Club')
        self.name = 'Biz Club'
        #Assertions
        self.assertTrue(isinstance(result,dict),"Record retrieved is not a dict")
        self.assertIsNotNone(result,"Record not found after updating")
        self.assertEqual(result['name'], 'Biz Club', f"Record updated incorrectly, result={result}")
        
    def test_retrieve_cca(self):
        """
        Tests if retrieve_cca function works
        """
        try:
            create_cca(self.name, self.type)
        except AttributeError:
            pass
            
        result = retrieve_cca(self.name)
        
        #Assertions
        self.assertTrue(isinstance(result,dict),"Record retrieved is not a dict")
        self.assertIsNotNone(result,"Record not found at all")
        self.assertEqual(result['name'], self.name, f"Record retrieved incorrectly, result={result}")

    def test_delete_record(self):
        """
        Tests if the delete_cca function works
        """
        try:
            create_cca(self.name, self.type)
        except AttributeError:
            pass
            
        delete_cca(self.name)
        #Assertions
        with self.assertRaises(AttributeError, msg = "CCA record not deleted"):
            retrieve_cca(self.name)
    
    def tearDown(self) -> None:
        """
        Runs after every test
        """
        self.conn.close()


class Test_Activity(TestCase):
    def setUp(self):
        """
        Runs before every test
        """
        #Set up connection to an in-memory SQLite database too for ensuring table creation
        self.account = get_account('qa')
        self.student = get_student('qa')
        self.activity = get_activity('qa')
        self.conn = sqlite3.connect(':memory:')
        self.cursor = self.conn.cursor()
        self.name = 'Walk For Rice'
        self.date = '14/11/24'
        self.location = 'Stadium'
        self.username = 'name'
        self.password = 'Password1'
        try:
            create_account(self.username, self.password)
            create_profile('John Doe','2328','abc@gmail.com','12345678','Bla Bla',self.username)
        except AttributeError:
            pass

        # Create the 'cca' table using direct SQL query
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS "activity" (
            "activity_id" INTEGER PRIMARY KEY,
            "name" TEXT NOT NULL UNIQUE,
            "date" TEXT NOT NULL, 
            "location" TEXT NOT NULL,
            "organiser_id" INTEGER,
            FOREIGN KEY ("organiser_id") REFERENCES account("student_id")
        );
        ''')
        self.conn.commit()

        #initialise tables
        init_tables(conn_factory('qa', ':memory:'))

    def test_table(self):
        """
        Test checks for presence of cca table
        """
        query = """
            SELECT name
            FROM sqlite_master
            WHERE  type='table' 
            AND name = ?;
            """
        params = ('activity',)
        self.cursor.execute(query,params)
        tables = self.cursor.fetchall()
        self.assertNotEqual(tables, [], msg="No 'cca' table created in database")

    def test_create_activity(self):
        create_activity(self.name,self.date,self.location,self.username)
        result = retrieve_activity(self.name)
        #Assertions
        self.assertTrue(isinstance(result,dict), "Record retrieved is not a dict")
        self.assertIsNotNone(result,"Record not inserted at all")
        self.assertEqual(result['name'], self.name, f"Record inserted incorrectly, result={result}")

    def test_update_activity(self):
        # try:
        #     create_activity(self.name,self.date,self.location,self.username)
        # except AttributeError:
        #     return self.activity
        
        update_activity(self.name, 'name', 'Wild Run')
        self.name = 'Wild Run'
        update_activity(self.name,'location','NYJC')
        self.location = 'NYJC'

        result = retrieve_activity(self.name)
        #Assertions
        self.assertTrue(isinstance(result,dict), "Record retrieved is not a dict")
        self.assertIsNotNone(result,"Record not inserted at all")
        self.assertEqual(result['name'], self.name, f"Record inserted incorrectly, result={result}")
        self.assertEqual(result['location'], self.location, f"Record inserted incorrectly, result={result}")

    def test_retrieve_activity(self):
        try:
            create_activity(self.name,self.date,self.location,self.username)
        except AttributeError:
            pass
        
        result = retrieve_activity(self.name)
        #Assertions
        self.assertTrue(isinstance(result,dict), "Record retrieved is not a dict")
        self.assertIsNotNone(result,"Record not inserted at all")
        self.assertEqual(result['name'], self.name, f"Record inserted incorrectly, result={result}")

    def test_delete_activity(self):
        try:
            create_activity(self.name,self.date,self.location,self.username)
        except AttributeError:
            pass

        delete_activity(self.name)
        #Assertions
        with self.assertRaises(AttributeError, msg = "CCA record not deleted"):
            retrieve_activity(self.name)
        
    def tearDown(self):
        self.conn.close()