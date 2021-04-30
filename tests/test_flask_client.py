import flask_unittest
import unittest
import flask.globals

from app import create_app, db
from app.models import User, Role


class FlaskTestCase(flask_unittest.ClientTestCase):
    app = create_app('testing')

    def setUp(self, client):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.tester = self.app.test_client()
        db.create_all()
        self.create_dummy_data(client)

    def create_dummy_data(self, client):
        employee_role = Role(name='employee')
        supervisor_role = Role(name='supervisor')
        hr_role = Role(name='hr')

        user_test_1 = User(email='employee@gmail.com', password='password',
                           full_name='Max Mustermann', role=employee_role)
        db.session.add_all([employee_role, supervisor_role,
                           hr_role, user_test_1])
        db.session.commit()

    def tearDown(self, client):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_login_status(self, client):
        response = self.tester.get('/login', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_login_correct_login(self, client):
        response = self.tester.post(
            '/login',
            data=dict(username="employee@gmail.com", password="password"),
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)

    def test_login_invalid_data(self, clientlf):
        response = self.tester.post(
            '/login',
            data=dict(username="false_email@gmail.com",
                      password="wrongpassword"),
        )
        self.assertLocationHeader(
            rv=response,
            expected_location='http://localhost/login',
        )


if __name__ == '__main__':
    unittest.main()
