from dbfunctions import *
from database import init_tables
from unittest import *
from auth import create_hash

#Instantiating table objects
account = get_account('qa')
student_profile = get_student('qa')
test_cca = get_cca('qa')
test_activity = get_activity('qa')

class Test_Account(TestCase):
    def setUp(self):
        # Set up connection to an in-memory SQLite database(jic)
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
    
    def test_create_account(self, account = account): #Account object taken in just in case for future testing
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
        def check_for_record(username: str, case: int) -> None:
            errors = {1: "\n\nTable Not Properly Functional:\n", 2: "\n\nInsert Method Not Properly Functional:\n"}
            error = errors[case]

            #Check for record in the table with the input username
            query = """
                SELECT *
                FROM 'account'
                WHERE  username = ?;
                """
            params = (username,)
            self.cursor.execute(query, params)
            self.connection.commit()
            row = self.cursor.fetchone()

            #Get all records in account table
            self.cursor.execute('SELECT * from Account')

            #Assertions
            self.assertIsNotNone(row,f"{error} Record not inserted at all, contents = {self.cursor.fetchall()}")
            self.assertEqual(row[1], username, f"{error} Record inserted incorrectly,contents = {self.cursor.fetchall()}")

        #Insert Record via manual sql query
        try:
            # create_account(username1, password1)
            hash, salt = create_hash(password1)
            self.cursor.execute("INSERT INTO Account (username, password, salt) VALUES (?, ?, ?)", (username1, hash, salt))
            self.connection.commit()
        except:
            self.fail(msg="Creating account does not work(Manual sql query)")

        #Check the record inserted via manual sql query
        check_for_record(username1, 1)

        #Insert another record via insert method of account
        try:
            #create_account(username2, password2)
            hash, salt = create_hash(password2)
            account.insert({'username': username2, 'password': hash, 'salt': salt})
            self.connection.commit()
        except:
            self.fail(msg="Creating account does not work at all(insert method)")
            
        #Check the record inserted via insert method of account
        check_for_record(username2, 2)
        


    

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