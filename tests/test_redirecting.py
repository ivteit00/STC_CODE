import flask_testing
import unittest
import flask.globals
from time import sleep

import app
from app.models import User, Role
from app import db


class RedirectTestCase(flask_testing.TestCase):

    def create_app(self):
        test_app = app.create_app('testing')
        self.app = test_app
        return test_app

    def setUp(self) -> None:

        self.app_context = self.app.app_context()
        self.app_context.push()
        self.tester = self.app.test_client()
        db.create_all()
        self.create_dummy_data()

    def create_dummy_data(self) -> None:
        """Creating dummy data for the database"""
        employee_role = Role(name='employee')
        supervisor_role = Role(name='supervisor')
        hr_role = Role(name='hr')

        user_test_1 = User(email='employee@gmail.com', password='password',
                           full_name='Max Mustermann', role=employee_role)
        db.session.add_all([employee_role, supervisor_role,
                           hr_role, user_test_1])
        db.session.commit()

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_login_works(self) -> None:
        """Testing if the server accepts the login with valid credential"""
        response = self.tester.post(
            '/login',
            data=dict(email='employee@gmail.com', password='password'),
            follow_redirects=True
        )
        self.assertRedirects(response, '/home')

    # def test_login_invalid_data(self) -> None:
    #     """Testing if the server rejects the login with invalid credentials"""
    #     response = self.tester.post(
    #         '/login',
    #         data=dict(username="false_email@gmail.com",
    #                   password="wrongpassword"),
    #     )
    #     # self.assertLocationHeader(
    #     #     rv=response,
    #     #     expected_location='http://localhost/login',
    #     # )
    #     self.assertTemplateUsed('login.html')
    