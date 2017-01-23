import json
from app import db
from flask import jsonify, request
from flask_restful import abort, Resource
from app.models.bucketlist_models import Users


class Register(Resource):
    """
GET: Obtain information about a User resource
POST: Create a new User resource and adds them to the db
    """

    def get(self):
        return jsonify({'message': "Welcome,to register,"
                        "send a POST request with a username, email and password"
                        "to /auth/register."})

    def post(self):
        data = json.loads(request.get_data(as_text=True))
        if not data:
                # Incase user doesn't pass anythin
            abort(400,
                  message="No parameters supplied, please make sure all fields are field")
        if len(data.keys()) < 3:
                # Incase a user doesn't pass all the 3 params
            abort(400,
                  message="Please make sure ALL parameters are filled")
        if not data['username'] or not data['username'] or not data['password']:
            abort(400,
                  message="Kindly fill in the missing field")

        username = data['username']
        email = data['email']
        password = data['password']

        if len(password) < 6:
            abort(400,
                  message="Password should be more than 4 characters")

        if '@' or '.' not in email:
            abort(400,
                  message="Please make sure you supplied a valid email")

        user = Users.query.filte_by(username=username).first()
        if user is not None:
            abort(400,
                  message="A user with that username exists!")

        try:
            new_user = Users(
                username=username,
                email=email,
                password=password
            )
            db.session.add(new_user)
            db.session.commit()
            return jsonify({
                'message': "{} added successfully".format(username)})
        except Exception as e:
        	abort(500, message="User not created")
