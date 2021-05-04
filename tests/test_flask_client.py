import flask_unittest
import unittest
import flask.globals
from time import sleep

from app import create_app, db
from app.models import User, Role


class FlaskTestCase(flask_unittest.ClientTestCase):
    app = create_app('testing')

    def setUp(self, client) -> None:
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.tester = self.app.test_client()
        db.create_all()
        self.create_dummy_data(client)

    def create_dummy_data(self, client) -> None:
        """Creating dummy data for the database"""
        employee_role = Role(name='employee')
        supervisor_role = Role(name='supervisor')
        hr_role = Role(name='hr')

        user_test_1 = User(email='employee@gmail.com', password='password',
                           full_name='Max Mustermann', role=employee_role)
        db.session.add_all([employee_role, supervisor_role,
                           hr_role, user_test_1])
        db.session.commit()

    def tearDown(self, client) -> None:
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_is_live(self, client) -> None:
        """Test if the web-application can be called"""
        response = self.tester.get('/', content_type='html/text')
        self.assertIsNotNone(response)

    def test_login_status(self, client) -> None:
        """Testing if the login page can be accessed"""
        response = self.tester.get('/login', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_access_without_login(self, client) -> None:
        """Test if the the home page can be accessed without logging in"""
        response = self.tester.get('/home', content_type='html/text')
        self.assertLocationHeader(
            rv=response,
            expected_location='http://localhost/login?next=%2Fhome')

    def test_access_restriction(self, client) -> None:
        pass


if __name__ == '__main__':
    unittest.main()
