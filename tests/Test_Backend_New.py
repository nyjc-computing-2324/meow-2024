import sqlite3
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
    
    def test_create_account(self):
        """
        Test checks whether the create_account function
        works.
        """
        #Initialise tables
        init_tables(conn_factory('qa', ':memory:'))

        #Test Case
        username = 'name1'
        password = 'Password1'

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
        create_account(username, password)

        #Check the record inserted via manual sql query
        check_for_record(username)        


    

    def tearDown(self):
        self.connection.close()
        
        
        

def login():
    pass


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


class Test_CCA(TestCase):
    def setUp(self):
        # Set up connection to an in-memory SQLite database(jic)
        self.cca = get_cca('qa')
        self.connection = sqlite3.connect(':memory:')
        self.cursor = self.connection.cursor()
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
        self.connection.commit()

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
        Test checks whether the create_account function
        works.
        """
        create_cca(self.name, self.type)

        result = retrieve_cca(self.name)
        #Assertions
        self.assertTrue(isinstance(result,dict))
        self.assertIsNotNone(result,f"Record not inserted at all, result = {result}")
        self.assertEqual(result['name'], self.name, f"Record inserted incorrectly, result={result}")

    def test_update_cca(self):
        create_cca(self.name, self.type)
        update_cca(self.name,'name','Biz Club')

        result = retrieve_cca('Biz Club')
        #Assertions
        self.assertTrue(isinstance(result,dict))
        self.assertIsNotNone(result,f"Record not inserted at all, result = {result}")
        self.assertEqual(result['name'], 'Biz Club', f"Record inserted incorrectly, result={result}")