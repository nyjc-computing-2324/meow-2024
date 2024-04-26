from dbfunctions import *
from unittest import *

#Instantiating table objects
student_account = get_account('qa')
test_student = get_student('qa')
test_cca = get_cca('qa')
test_activity = get_activity('qa')

def test_create_account(username: str, password: str):
    create_account(username, password)

def login():
    pass