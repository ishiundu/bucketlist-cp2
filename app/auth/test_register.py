import json
import unittest
from app import db
from app.models.bucketlist_models import Users
from app.test_config import GlobalTestCase
from flask import url_for


class RegistrationTest(GlobalTestCase):

    def setUp(self):
        db.drop_all()
        db.create_all()
        user = Users(
            username='paul',
            email='paul@andela.com',
            password='12345')
        db.session.add(user)
        db.session.commit()
        

    def test_register_endpoint(self):
        response = self.client.get(
            url_for('register'))
        data = json.loads(response.get_data(as_text=True))
        self.assert_status(response, 200)
        self.assertIn('Welcome,to register', data['message'])

    def test_registration_of_a_new_user(self):
        response = self.client.post(
            url_for('register'),
            data=json.dumps(
                {'username': 'johndoe',
                 'password': 'john123',
                 'email': 'johndoe123@andela.com'}),
            content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertIsNotNone(data)
        self.assertIn("added successfully", data['message'])

    def test_registration_of_existing_user(self):
        response = self.client.post(
            url_for('register'),
            data=json.dumps(
                {'username': 'paul',
                 'email': 'paul@andela.com',
                 'password': '12345'
                 }),
            content_type='application/json')
        data = json.loads(response.get_data(as_text=True))
        self.assertIsNotNone(data)
        self.assertIn("user with that username exists", data['message'])

    def test_registration_with_short_password(self):
        response = self.client.post(
            url_for('register'),
            data=json.dumps({
                'username': 'Restapi',
                'email': 'restapi@gmail.com',
                'password': '911'}),
            content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.get_data(as_text=True))
        self.assertIsNotNone(data)
        self.assertIn("Password should be more than 4 characters", data['message'])


if __name__ == '__main__':
    unittest.main()
