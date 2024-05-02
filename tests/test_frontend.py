from unittest import *
from main import app
import view

class Test_Frontend(TestCase):

    def setUp(self):
        app.testing = True
        view.completed = True
        self.app = app.test_client()
        self.paths = ['/', '/temp', '/home', '/about', '/login', '/register']

    def test_request_load_successfully(self):
        """
        Checks whether all the routes load successfully without error/unexpected
        redirection
        """
        for path in self.paths:
            try:
                self.app.get(path)
            except NotImplementedError:
                continue
            response = self.app.get(path)
            self.assertEqual(response.status_code, 200, msg=f"{path} failed to load.")
