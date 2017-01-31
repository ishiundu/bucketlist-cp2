import json

import unittest
from app import db
from app.models.bucketlist_models import Users
from app.test_config import GlobalTestCase
from flask import url_for


class LoginTest(GlobalTestCase):
    def setUp(self):
        db.drop_all()
        db.create_all()
        user = Users(
            username='johndoe',
            email='johndoe123@andela.com',
            password='john123')
        db.session.add(user)
        db.session.commit()

    def test_index_endpoint(self):
        response = self.client.get(url_for('home'))
        data = json.loads(response.get_data(as_text=True))
        self.assert_status(response, 200)

    def test_login_end_point(self):
        response = self.client.get(url_for('login'))
        data = json.loads(response.get_data(as_text=True))
        self.assert_status(response, 200)
        self.assertEqual('To login,send a POST request to /auth/login',
                         data['message'])

    def test_correct_login_credentials(self):
        response = self.client.post(
            url_for('login'),
            data=json.dumps(
                {"username": "johndoe",
                 "password": "john123"}),
            content_type='application/json')
        data = json.loads(response.get_data(as_text=True))
        self.assertIn("Welcome", data['message'])

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
        self.assertIn("User does not exist", data['message'])

    def test_login_with_empty_username_or_password(self):
        response = self.client.post(
            url_for('login'),
            data=json.dumps(
                {'username': '',
                 'password': ''}),
            content_type='application/json')
        self.assert_status(response, 400)
        data = json.loads(response.get_data(as_text=True))
        self.assertIsNotNone(data)
        self.assertIn("Kindly fill in the missing details",
                      data['message'])


if __name__ == '__main__':
    unittest.main()
