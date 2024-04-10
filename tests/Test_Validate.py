from unittest import *
from validate import *
from database import *
#IMPORTANT Please Read
"""
We will be using the unittest module instead to test frontend and backend.
Using this module follows a similar OOP structure to the classes we made last session 
One key difference is that you need to inherit from the 'unittest.TestCase' baseclass
Methods must also start with 'test' as below, else unittest can't recognise and run them

Read these guides to familiarise yourselves:

DataQuest Simple Guide: https://www.dataquest.io/blog/unit-tests-python/

unittest Documentation: https://docs.python.org/3/library/unittest.html
"""

class Test_Validate(TestCase):

    def setUp(self):
        """
        Sample username/password values for testing, you guys
        can add more values to test more cases
        """
        #username test cases
        self.validname = 'aBc @123_beAnsta|k'
        self.validname_allspaces = '                            '

        self.invalidname_notascii = 'ABCD二十八'
        self.invalidname_notprintable = 'John \t Doe \n Smith'
        self.invalidname_empty = ''

        #password test cases
        self.validpassword = 'Abcd1234'
        self.validpassword_verylong = 'qwertty122345iuoUIOOPAHJKDLKGLBNZm2394879jLKJFMMNXKSJi4839902904jdsjlLKJLKJLJBKPPQIWOOIEMMJjmxznm4nmmnzx80zx'
        self.validpassword_specialcharacters = 'Ab1!@#$%^&*()_+-={}[]|:;"hello"<>?,./`~'

        self.invalidpassword_noupper = 'abcdsf1233'
        self.invalidpassword_nolower = 'ABCEF123'
        self.invalidpassword_nodigit = 'ABCDefgh'
        self.invalidpassword_tooshort = 'Ab1'
        self.invalidpassword_empty = ''
        self.invalidpassword_notascii = 'ABCd二十八28'
        self.invalidpassword_notprintable = 'ABCdef \t 123 \n 456'
        self.invalidpassword_withspaces = 'ABcd 12 34'



    def test_username_isvalid(self):
        """
        Tests the username_isvalid method on validate.py
        """
        self.assertTrue(username_isvalid(self.validname),'Username should be valid.')
        self.assertTrue(self.validname_allspaces, 'Username should be valid even if it contains all spaces')

        self.assertFalse(username_isvalid(self.invalidname_notascii),'Username should be invalid: Username contains non-ASCII characters.')
        self.assertFalse(username_isvalid(self.invalidname_notprintable),'Username should be invalid: Username contains non-printable characters.')
        self.assertFalse(username_isvalid(self.invalidname_empty), 'Username should be invalid: Username is empty string.')


    def test_password_isvalid(self):
        """
        Tests the password_isvalid method on validate.py
        """
        self.assertTrue(password_isvalid(self.validpassword), 'Password should be valid.')

        self.assertTrue(password_isvalid(self.validpassword_verylong), 'Password should be valid even though it is very long.')
        self.assertTrue(password_isvalid(self.validpassword_specialcharacters), 'Password should be valid even though it contains special characters.')

        self.assertFalse(password_isvalid(self.invalidpassword_noupper), 'Password should be invalid: There are no uppercase characters.')
        self.assertFalse(password_isvalid(self.invalidpassword_nolower), 'Password should be invalid: There are no lowercase characters.')
        self.assertFalse(password_isvalid(self.invalidpassword_nodigit), 'Password should be invalid: There are no ASCII numbers.')
        self.assertFalse(password_isvalid(self.invalidpassword_tooshort), 'Password should be invalid: Password is too short.')

        self.assertFalse(password_isvalid(self.invalidpassword_empty), 'Password should be invalid: Password is empty (an empty string).')
        self.assertFalse(password_isvalid(self.invalidpassword_notascii), 'Password should be invalid: Password contains non-ASCII characters.')
        self.assertFalse(password_isvalid(self.invalidpassword_notprintable), 'Password should be invalid: Password contains newline and tab characters, which are non-printable.')
        self.assertFalse(password_isvalid(self.invalidpassword_withspaces), 'Password should be invalid: Password contains spaces.')


