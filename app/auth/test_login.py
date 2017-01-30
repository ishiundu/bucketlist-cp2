import json

import unittest
from app import db
from app.models.bucketlist_models import Users
from app.test_config import GlobalTestCase
from flask import url_for


class LoginTest(GlobalTestCase):
    def SetUp(self):
        db.create_all()
        user = Users(
            username='johndoe',
            email='johndoe123@andela.com',
            password='john123')
        db.session.add(user)
        db.session.commit()

    def test_index_endpoint(self):
        response = self.client.get('/api/v1')
        data = json.loads(response.get_data(as_text=True))
        self.assert_status(response, 200)
        self.assertIn('Hello welcome to the number one Bucket List API',
                      data['message'])

    def test_login_end_point(self):
        response = self.client.get('api/v1/auth/login')
        data = json.loads(response.get_data(as_text=True))
        self.assert_status(response, 200)
        self.assertEqual('To login,send a POST request to /auth/login',
                         data['message'])

    def test_correct_login_credentials(self):
        """Here we test if the user is passing the appropriate credentials"""
        response = self.client.post(
            url_for('login'),
            data=json.dumps(
                {'username': 'johndoe',
                 'password': 'john123'}),
            content_type='application/json')
        self.assert_status(response, 400)
        data = json.loads(response.get_data(as_text=True))
        self.assertIsNotNone(data)
        self.assertIn("Welcome Ian", data['message'])

    def test_login_with_non_existent_user(self):
        response = self.client.post(
            url_for('login'),
            data=json.dumps(
                {'username': 'Lucy',
                 'password': 'lucy'}),
            content_type='application/json')
        self.assert_status(response, 400)
        data = json.loads(response.get_data(as_text=True))
        self.assertIsNotNone(data)
        self.assertIn("Sorry User doesn't exist", data['message'])

    def test_login_with_empty_username_or_password(self):
        """Here we test an instance where a user
        does not provide a username/password"""
        response = self.client.post(
            url_for('login'),
            data=json.dumps(
                {'username': '',
                 'password': ''}),
            content_type='application/json')
        self.assert_status(response, 400)
        data = json.loads(response.get_data(as_text=True))
        self.assertIsNotNone(data)
        self.assertIn("Please fill in the fields",
                      data['message'])

    def tearDown(self):
        db.session.close_all()
        db.drop_all()


if __name__ == '__main__':
    unittest.main()
