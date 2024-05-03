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
        self.cursor = self.conn.cursor()
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
        update_profile(self.username, "name", self.name2)
        update_profile(self.username, "name", self._class2)
        record1 = retrieve_profile(self.username)
        self.assertEqual(type(record), dict, "Retrieve does not return dictionary")
        self.assertNotEqual(record["name"], record1["name"], "Update function failed, name update unsuccessful")
        self.assertNotEqual(record["class"], record1["class"], "Update function failed, class update unsuccessful")

    def test_retrieve_profile(self):
        record = retrieve_profile(self.username)
        self.assertEqual(type(record), dict, "Retrieve does not return a dictionary")
        self.assertEqual(record["class"], self._class1, "Retrieved incorrect information")

    def test_delete_profile(self):
        delete_profile(self.username)
        try:
            result = retrieve_profile(self.username)
            self.assertNotEqual(type(result),dict, "Delete function failed")
        except AttributeError:
            self.assertEqual(1,1,"idk how this one even fails but good job if it does i guess")

    def tearDown(self) -> None:
        self.cursor.execute("""
            DROP TABLE "student"
            """)
        self.conn.close()
    

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