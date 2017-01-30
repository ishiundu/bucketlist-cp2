import json
import unittest
from app import db
from app.models.bucketist_models import Users
from app.test_config import GlobalTestCase
from flask import url_for


class RegistrationTest(GlobalTestCase):

    def setUp(self):
        db.create_all()

    def test_register_endpoint(self):
        response = self.client.get(
            url_for('register'))
        data = json.loads(response.get_data(as_text=True))
        self.assert_status(response, 200)
        self.assertEqual('To register, send a POST request with your username, password and email to /auth/register',
                         data['message'])

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
        self.assertIn("User, created successfully",
                      data['message'])

    def test_registration_of_existing_user(self):
        user = Users(
            username='johndoe',
            email='john123@gmail.com',
            password='john')
        db.session.add(user)
        db.session.commit()
        response = self.client.post(
            url_for('register'),
            data=json.dumps(
                {'username': 'johndoe',
                 'email': 'johndoe123@andela.com',
                 'password': 'john123'
                 }),
            content_type='application/json')
        data = json.loads(response.get_data(as_text=True))
        self.assertIsNotNone(data)
        self.assertIn("That user already exists!",
                      data['message'])

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
        self.assertIn("Your password doesnot meet the specified requirements",
                      data['message'])

    def tearDown(self):
        db.session.close_all()
        db.drop_all()


if __name__ == '__main__':
    unittest.main()
