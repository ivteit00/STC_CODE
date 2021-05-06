import unittest
from flask import current_app
from app import create_app, db


class BasicTestCases(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exists(self):
        """Test if create_app function works correctly"""
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        """Test if the configuration is right"""
        self.assertTrue(current_app.config['TESTING'])


if __name__ == '__main__':
    unittest.main()
