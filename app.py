from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
from pymongo import MongoClient
import os
from dotenv import load_dotenv
import hashlib
import datetime

load_dotenv()

app = Flask(__name__)
jwt = JWTManager(app)
app.config['JWT_SECRET_KEY'] = 'Your_Secret_Key'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)

client = MongoClient(
    os.environ.get('MONGO_HOST'),
    int(os.environ.get('MONGO_PORT')),
    username=os.environ.get('MONGO_USERNAME'),
    password=os.environ.get('MONGO_PASSWORD')    
)

db = client["animaixpert"]
users_collection = db["users"]

@app.route("/")
def hello_world():
    return os.environ.get('MONGO_USERNAME')

@app.route("/register", methods=["POST"])
def register():
    new_user = request.get_json() # store the json body request
    new_user["password"] = hashlib.sha256(new_user["password"].encode("utf-8")).hexdigest() # encrpt password
    
    check_username = users_collection.find_one({"username": new_user["username"]}) # check if username exist
    check_email = users_collection.find_one({"mail": new_user["mail"]}) # check if mail exist
    
    if not check_username and not check_email:
        users_collection.insert_one(new_user)
        return new_user, 201
    elif check_username:
        return jsonify({'msg': 'Username already exists'}), 409
    else:
        return jsonify({'msg': 'Email already exists'}), 409

@app.route("/login", methods=["POST"])
def login():
	login_details = request.get_json() # store the json body request
	user_from_db = users_collection.find_one({'username': login_details['username']})  # search for user in database

	if user_from_db:
		encrpted_password = hashlib.sha256(login_details['password'].encode("utf-8")).hexdigest()
		if encrpted_password == user_from_db['password']:
			access_token = create_access_token(identity=user_from_db['username']) # create jwt token
			return jsonify(access_token=access_token), 200

	return jsonify({'msg': 'The username or password is incorrect'}), 401

@app.route("/user", methods=["GET"])
@jwt_required()
def profile():
    print("HI")
    current_user = get_jwt_identity() # Get the identity of the current user
    print(f"USERNAME: {current_user}") 
    user_from_db = users_collection.find_one({'username' : current_user})
    if user_from_db:
        del user_from_db['_id'], user_from_db['password'] # delete data we don't want to return
        return jsonify({'profile' : user_from_db }), 200
    else:
        return jsonify({'msg': 'Profile not found'}), 404


if __name__ == '__main__':
	app.run(debug=True)