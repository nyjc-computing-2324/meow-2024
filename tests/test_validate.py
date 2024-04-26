from unittest import *
from validate import *
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
        Sets up the test cases to be used in unit test methods.
        """
        #username test cases
        self.validname = 'aBc @123_beAnsta|k'
        self.validname_allspaces = '                            '
        self.invalidname_notascii = 'ABCD二十八'
        self.invalidname_notprintable = 'John\tDoe\nSmith'
        self.invalidname_empty = ''

        #Password test cases
        #Valid
        self.validpassword = 'Abcd1234'
        self.validpassword_verylong = 'qwertty122345iuoUIOOPAHJKDLKGLBNZm2394879jLKJFMMNXKSJi4839902904jdsjlLKJLKJLJBKPPQIWOOIEMMJjmxznm4nmmnzx80zx'
        self.validpassword_specialcharacters = 'Ab1!@#$%^&*()_+-={}[]|:;"hello"<>?,./`~'
        #Invalid
        self.invalidpassword_noupper = 'abcdsf1233'
        self.invalidpassword_nolower = 'ABCEF123'
        self.invalidpassword_nodigit = 'ABCDefgh'
        self.invalidpassword_tooshort = 'Ab1'
        self.invalidpassword_empty = ''
        self.invalidpassword_notascii = 'ABCd二十八28'
        self.invalidpassword_notprintable = 'ABCdef\t123\n456'
        self.invalidpassword_withspaces = 'ABcd 12 34'

        #user validation test case
        test_account = Account(":memory:")
        self.user_a = {'Name':'AAAAA', 'Password':'ABCDefg1234'}
        self.user_b = {'Name':'Beez Nuts', 'Password':'B33z_Nutz'}

        test_account.insert(self.user_a['Name'], self.user_a['Password'])
        test_account.insert(self.user_b['Name'], self.user_b['Password'])



    def test_username_isvalid(self):
        """
        Tests the username_isvalid method on validate.py
        """
        #Valid test cases
        self.assertTrue(username_isvalid(self.validname),'Username should be valid.')
        self.assertFalse(self.invalidname_allspaces, 'Username should be invalid: Username cannot contain spaces.')

        #Invalid test cases
        self.assertFalse(username_isvalid(self.invalidname_notascii),'Username should be invalid: Username contains non-ASCII characters.')
        self.assertFalse(username_isvalid(self.invalidname_notprintable),'Username should be invalid: Username contains non-printable characters.')
        self.assertFalse(username_isvalid(self.invalidname_empty), 'Username should be invalid: Username is empty string.')

    
    def test_password_isvalid(self):
        """
        Tests the password_isvalid method on validate.py.
        Password SHOULD be 8 characters or longer, and must contain at least 1 uppercase, lowercase, and number.
        Password CANNOT contain new line, tab, non-ASCII, spaces, and cannot be empty.
        """
        #Valid test cases
        self.assertTrue(password_isvalid(self.validpassword), 'Password should be valid.')

        self.assertTrue(password_isvalid(self.validpassword_verylong), 'Password should be valid even though it is very long.')
        self.assertTrue(password_isvalid(self.validpassword_specialcharacters), 'Password should be valid even though it contains special characters.')

        #Invalid test cases
        self.assertFalse(password_isvalid(self.invalidpassword_noupper), 'Password should be invalid: There are no uppercase characters.')
        self.assertFalse(password_isvalid(self.invalidpassword_nolower), 'Password should be invalid: There are no lowercase characters.')
        self.assertFalse(password_isvalid(self.invalidpassword_nodigit), 'Password should be invalid: There are no ASCII numbers.')
        self.assertFalse(password_isvalid(self.invalidpassword_tooshort), 'Password should be invalid: Password is too short.')

        self.assertFalse(password_isvalid(self.invalidpassword_empty), 'Password should be invalid: Password is empty (an empty string).')
        self.assertFalse(password_isvalid(self.invalidpassword_notascii), 'Password should be invalid: Password contains non-ASCII characters.')
        self.assertFalse(password_isvalid(self.invalidpassword_notprintable), 'Password should be invalid: Password contains newline and tab characters, whcih are non-printable.')
        self.assertFalse(password_isvalid(self.invalidpassword_withspaces), 'Password should be invalid: Password contains spaces.')


    def test_user_isvalid(self):
        """
        Tests the user_isvalid method on validate.py
        """
        self.assertTrue(user_isvalid(self.user_a['Name'], self.user_a["Password"]), 'User should be valid (User A).')
        self.assertTrue(user_isvalid(self.user_b['Name'], self.user_b["Password"]), 'User should be valid (User B).')

        self.assertFalse(user_isvalid(self.user_a['Name'], self.user_a["Name"]), 'User should be not valid: Second argument uses the Username instead of the Password.')
        self.assertFalse(user_isvalid(self.user_a['Name'], self.user_b["Password"]), 'User should be not valid: User A Username with User B Password.')
        self.assertFalse(user_isvalid(self.user_a['Password'], self.user_a["Name"]), 'User should be not valid: Username and Password arguments are swapped.')


