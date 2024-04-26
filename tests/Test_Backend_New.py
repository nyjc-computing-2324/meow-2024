from dbfunctions import *
from unittest import *

#Instantiating table objects
student_account = get_account('qa')
student_profile = get_student('qa')
test_cca = get_cca('qa')
test_activity = get_activity('qa')

def test_create_account(username: str, password: str):
    create_account(username, password)
    
        

def login():
    pass


class Test_Profile(TestCase):
    def setUp(self):
        self.name1 = 'abcdefghi!'
        self._class1 = '2328'
        self.email1 = 'name@gmail.com'
        self.name2 = 'qwertyuiop'
        self._class1 = '2401'
        create_profile(self.name1, self._class1, self.email1, 1)

    def tearDown(self) -> None:
    return super().tearDown()