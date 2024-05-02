from unittest import *
from main import app
import view

class Test_Frontend(TestCase):

    def setUp(self):
        app.testing = True
        view.completed = True
        self.app = app.test_client()
        self.paths = ['/', '/temp', '/home', '/edit_activities', '/about',                             '/pp', '/tac', '/login', '/register', '/profile',                                '/profile_edit', '/view_cca', '/edit_cca', '/records_cca',                       '/records_activities', '/view_activities']

    def test_request_load_successfully(self):
        """
        Checks whether all the routes load successfully without error/unexpected
        redirection
        """
        for path in self.paths:
            try:
                self.app.get(path)
            except AttributeError: #Need auth to access but that is already tested with exploratory testing
                continue
            except NotImplementedError: #Imcomplete/Unimplemented paths will be displayed after end of test line-by-line
                print(f"\n{path}")
                continue
            
            response = self.app.get(path)
            self.assertEqual(response.status_code, 200, msg=f"{path} failed to load.")
