import json
import jwt
from app.models.bucketlist_models import Users
from config import config
from datetime import datetime, timedelta
from flask import jsonify, request
from flask_restful import abort, Resource


class Index(Resource):

    def get(self):
        return({"message": "Welcome to the Bucketlist API"
                "Register a new User by"
                "sending a POST request to auth/register"
                "Login by sending a post request to"
                "POST auth/login to get started"})


class Login(Resource):
    def get(self):
        return jsonify({"message": "To login,"
        	"send a post request to auth/login"})

    def post(self):
    	data = json.loads(request.get_data(as_text=True))
    	if not data:
    		abort(
    			400,
    			message="No parameters passed. Please fill all fields")
		username = data['username']
		password = data['password']

		if not username or password:
			abort(400,
				message="Kindly fill in the missing details")

		user = Users.query.filter_by(username=username).first()
		if user is None:
			abort(400, message="User doesnot exist")
		if user.verify_password(password):
			payload = {
				'sub' : user.user_id,
				'exp' : datetime.utcnow() + timedelta(minute=30)
			}
			token = jwt.encode(payload, Config.SECRET_KEY, algorithm='HS256')
			return jsonify({"message" : "Welcome {}".format(user.username),
				            "token" : token.decode('utf-8')})
		abort(400, message="Invalid password")
