from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager,get_jwt_identity,jwt_required,create_access_token
from flask_bcrypt import Bcrypt
from pymongo import MongoClient
import os
from dotenv import load_dotenv
import hashlib
import datetime
from bson.objectid import ObjectId

app = Flask(__name__)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)
app.config['JWT_SECRET_KEY'] = 'Your_Secret_Key'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)
load_dotenv()

client = MongoClient(
    os.environ.get('MONGO_HOST'),
    int(os.environ.get('MONGO_PORT')),
    username=os.environ.get('MONGO_USERNAME'),
    password=os.environ.get('MONGO_PASSWORD')    
)


@app.route("/")
def hello_world():
    return os.environ.get('MONGO_USERNAME')

db = client["animaixpert"]
users_collection = db["users"]


@app.route("/register", methods=["POST"])
def register():
    new_user = request.get_json() # store the json body request
    new_user["password"] = hashlib.sha256(new_user["password"].encode("utf-8")).hexdigest() # encrpt password
    #doc = users_collection.find_one({"username": new_user["username"]}) # check if user exist
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
    





@app.route('/change_password', methods=['PUT'])
@jwt_required()
def change_password():
    current_user_id = get_jwt_identity()
    user = users_collection.find_one({'username' : current_user_id})
    if not user:
        return jsonify({'message': 'User not found'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'message': 'No input data provided'}), 400

    password = data.get('password')
    password_hashed=hashlib.sha256(password.encode("utf-8")).hexdigest()
    new_password = data.get('new_password')

    if user['password']== password_hashed:
        return jsonify({'message': 'Invalid password'}), 400

    new_hashed_password = hashlib.sha256(data['new_password'].encode("utf-8")).hexdigest()
    users_collection.update_one({'username' : current_user_id}, {'$set': {'password': new_hashed_password}})

    return jsonify({'message': 'Password updated successfully'}), 200

    


if __name__ == '__main__':
    app.run(debug=True)