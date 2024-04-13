from unittest import *
from main import app
import view
import requests
from bs4 import BeautifulSoup
#IMPORTANT Please Read
"""
We will be using the unittest module instead to test frontend and backend.
Using this module follows a similar OOP structure to the classes we made last session 
One key difference is that you need to inherit from the 'unittest.TestCase' baseclass
Methods must also start with 'test' as below, else unittest can't recognise and run them

Read these guides to familiarise yourselves:

DataQuest Simple Guide: https://www.dataquest.io/blog/unit-tests-python/

unittest Documentation: https://docs.python.org/3/library/unittest.html

Here is an example of how frontend testing is implemented,
This route tested returns a redered html page containing 'Hello, World!':

class TestFlaskRoutes(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_hello_route(self):
        response = self.app.get('/')
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['message'], 'Hello, World!')

if __name__ == '__main__':
    unittest.main()
"""


class Test_Frontend(TestCase):

    def setUp(self):
        app.testing = True
        view.completed = True
        self.app = app.test_client()
        self.paths = ['/', '/temp', '/home', '/about', '/login', '/register']

    def test_request_load_successfully(self):
        for path in self.paths:
            response = self.app.get(path)
            self.assertEqual(response.status_code, 200, msg=f"{path} failed to load.")

    def test_temp(self):
        r = requests.get('https://meow-dev.replit.app' + '/temp')
        content = r.content
        soup = BeautifulSoup(content, 'html.parser')
        # print(soup.prettify())
        title = soup.find_all('title')[0].get_text()
        self.assertEqual(title, "Meow")
        
        
    # def test_index_loads_successfully(self):
    #     response = self.app.get('/')
    #     data = response.get_json()
    #     self.assertEqual(response.status_code, 200)
        

    # def test_temp_loads_successfully(self):
    #     response = self.app.get('/temp')
    #     data = response.get_json()
    #     self.assertEqual(response.status_code, 200)

    # def test_home_loads_successfully(self):
    #     response = self.app.get('/home')
    #     data = response.get_json()
    #     self.assertEqual(response.status_code, 200)

    # def test_about_loads_successfully(self):
    #     response = self.app.get('/about')
    #     data = response.get_json()
    #     self.assertEqual(response.status_code, 200, msg=f"")

    # def test_login_loads_successfully(self):
    #     response = self.app.get('/login')
    #     data = response.get_json()
    #     self.assertEqual(response.status_code, 200)

    # def test_register_loads_successfully(self):
    #     response = self.app.get('/register')
    #     data = response.get_json()
    #     self.assertEqual(response.status_code, 200)


