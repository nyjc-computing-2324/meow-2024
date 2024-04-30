from dbfunctions import *
from database import init_tables
from unittest import *

#Instantiating table objects
account = get_account('qa')
student_profile = get_student('qa')
test_cca = get_cca('qa')
test_activity = get_activity('qa')

class Test_Account(TestCase):
    
    def test_create_account(self, account = account): #Account object taken in just in case for future testing
        #Initialise tables
        init_tables(conn_factory('qa', ':memory:'))

        #Test Case
        username = 'name'
        password = 'Password1'

        #Check for presence of account table
        with sqlite3.connect(':memory:') as conn:
            cursor = conn.cursor()
            query = """
                SELECT name
                FROM sqlite_master
                WHERE  type='table' 
                AND name = ?;
                """
            params = ('account',)
            cursor.execute(query,params)
            tables = cursor.fetchall()
            self.assertNotEqual(tables, [], msg="No 'account' table created in database")

            #Call for create_account within the same conn
            create_account(username, password)

            #Check for record in the table with the input username
            query = """
                SELECT *
                FROM 'account'
                WHERE  username = ?;
                """
            params = (username,)
            cursor.execute(query, params)
            conn.commit()
            row = cursor.fetchone()
        self.assertIsNotNone(row,'Record not inserted at all')
        self.assertEqual(row[1], username, "Record inserted incorrectly")
        
        
        

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