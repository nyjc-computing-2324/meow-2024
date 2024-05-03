from typing import Optional
from unittest.case import _AssertRaisesContext
from dbfunctions import *
from database import init_tables
from unittest import *
from auth import create_hash

#Instantiating table objects
# student_profile = get_student('qa')
# test_cca = get_cca('qa')
# test_activity = get_activity('qa')

class Test_Account(TestCase):
    def setUp(self):
        # Set up connection to an in-memory SQLite database(jic)
        self.account = get_account('qa')
        # self.connection = sqlite3.connect(':memory:')
        # self.cursor = self.connection.cursor()

        # Create the 'Account' table using direct SQL query
        # self.cursor.execute('''
        # CREATE TABLE IF NOT EXISTS "account" (
        # "account_id" INTEGER PRIMARY KEY,
        # "username" TEXT NOT NULL UNIQUE,
        # "password" TEXT NOT NULL,
        # "salt" BYTES NOT NULL
        # );
        # ''')
        # self.connection.commit()
    
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
        #Initialise tables
        init_tables(conn_factory('qa', ':memory:'))

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


    def test_login(self):
        # if not self.result_create_account.wasSuccessful():
        #     self.skipTest("Skipping test condition as account creation does not work")

        right_username_login = 'rightnamelogin'
        right_password_login = 'RightPa55wordl0gin'
        wrong_username_login = 'wrongnamelogin'
        wrong_password_login = 'WrongPa55wordl0gin'

        create_account(right_username_login, right_password_login)
        
        self.assertTrue(login(right_username_login, right_password_login), 'Login should work.')
        self.assertFalse(login(right_username_login, wrong_password_login), 'Login should not work: Wrong password.')
        self.assertFalse(login(wrong_username_login, right_password_login), 'Login should not work: Wrong username.')
        self.assertFalse(login(wrong_username_login, wrong_password_login), 'Login should not work: Wrong username and password.')


    def test_username_taken(self):
        taken_username = 'alreadytakenname'
        password_of_taken_username = 'P4ssword0fTakenName'
        not_taken_username = 'notyettakenname'

        create_account(taken_username, password_of_taken_username)

        self.assertTrue(username_taken(taken_username), 'Username should already be taken.')
        self.assertFalse(username_taken(not_taken_username), 'Username is not taken.')

    
    def test_retrieve(self):
        username_retrieve = 'usernameretrieve'
        password_retrieve = 'P4ssw0rdRetrieve'

        wrong_username_retrieve = 'wrongretrieve'

        create_account(username_retrieve, password_retrieve)
        retrieved_data = retrieve_account(username_retrieve)
        
        self.assertEqual(retrieved_data['username'], username_retrieve, 'Username retrieved is wrong.')
        self.assertEqual(retrieved_data['password'], password_retrieve, 'Password retrieved is wrong.')
        self.assertRaises(AttributeError, retrieve_account, wrong_username_retrieve)


    def test_delete_account(self):
        """
        This test assumes that create_account() and retrieve_account() works.
        """
        username = 'tobedeleted'
        password = '2Bdeleted'

        create_account(username, password)

        delete_account(username)
        self.assertRaises(AttributeError, retrieve_account, username)

        
    def test_update_account(self):
        """
        This test assumes that create_account(), retrieve_account(), and delete_account() works.
        """

        old_username = 'oldusername'
        old_password = 'OldP4ssw0rd'

        new_username = 'newusername'
        new_password = 'NewP4ssw0rd'

        #Case 1: Change Password
        create_account(old_username, old_password)
        update_account(old_username, 'password', new_password )
        self.assertEqual(retrieve_account(old_username)['password'], new_password, 'Password update failed.')

        delete_account(old_username)
        
        #Case 2: Change Username
        create_account(old_username, old_password)
        update_account(old_username, 'username', new_username )
        self.assertEqual(retrieve_account(new_username)['username'], new_username, 'Username update failed.')
        



    # def tearDown(self):
    #     self.connection.close()
        
        
        



    
# class Test_Profile(TestCase):
#     def setUp(self):
#         self.name1 = 'abcdefghi!'
#         self._class1 = '2328'
#         self.email1 = 'name@gmail.com'
#         self.name2 = 'qwertyuiop'
#         self._class1 = '2401'
#         create_profile(self.name1, self._class1, self.email1, 1)

#     def tearDown(self) -> None:
#     return super().tearDown()