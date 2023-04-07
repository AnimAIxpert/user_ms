import json
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager,get_jwt_identity,jwt_required,create_access_token
#from flask_mail import Mail, Message
from pymongo import MongoClient
from bson import json_util
import os
from dotenv import load_dotenv
import hashlib
import datetime
import random
import string
#import smtplib
from bson.objectid import ObjectId
from email.mime.text import MIMEText
from mongoClient import client

app = Flask(__name__)
jwt = JWTManager(app)
app.config['JWT_SECRET_KEY'] = 'Your_Secret_Key'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)
load_dotenv()




# Initialisez l'extension Flask-Mail
# app.config.update(
#     MAIL_SERVER='smtp.gmail.com',
#     MAIL_PORT=465,
#     MAIL_USE_TLS= False,
#     MAIL_USE_SSL = True,
#     MAIL_USERNAME = 'sebasdeloco@gmail.com',
#     MAIL_PASSWORD = 'SEBASdeloco12'
# )

#app.config['MAIL_SERVER'] = 'smtp@gmail.com' #os.environ.get('MAIL_SERVER')
#app.config['MAIL_PORT'] = 465 #os.environ.get('MAIL_PORT')
#app.config['MAIL_USE_SSL'] = True#os.environ.get('MAIL__USE_SSL')
#app.config['MAIL_USERNAME'] = 'sebasdeloco@gmail.com'#os.environ.get('MAIL_USERNAME')
#app.config['MAIL_PASSWORD'] = 'SEBASdeloco12'#os.environ.get('MAIL_PASSWORD')
#app.config['MAIL_DEFAULT_SENDER'] ='sebasdeloco@gmail.com '#os.environ.get('MAIL_DEFAULT_SENDER')
#app.config['MAIL_USE_TLS'] = False
#mail = Mail(app)


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
        new_user['email_confirmed'] = False
        users_collection.insert_one(new_user)
        #send_email_confirmation(new_user['mail'])
        new_user = users_collection.find_one({"username": new_user["username"]})
        json_response =json.loads(json_util.dumps(new_user))
        
        print(json_response)
        return json_response, 201
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

#problem of email !!!!!!!
@app.route('/forgot_password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No input data provided'}), 400

    email = data.get('mail')
    user = users_collection.find_one({'mail': email})
    if not user:
        return jsonify({'message': 'User not found'}), 404

    # Génère un jeton aléatoire pour la réinitialisation du mot de passe
    token = ''.join(random.choices(string.ascii_uppercase + string.digits, k=32))
    users_collection.update_one({'_id': user['_id']}, {'$set': {'reset_password_token': token}})

    # Envoie un e-mail de réinitialisation du mot de passe à l'utilisateur
    #msg = Message('Réinitialisation du mot de passe', recipients=[email])
    #msg.body = f"Pour réinitialiser votre mot de passe, cliquez sur ce lien : http://localhost:5000/reset_password?token={token}"
    #mail.send(msg)

    return jsonify({'message': 'Un e-mail de réinitialisation du mot de passe a été envoyé'}), 200

@app.route('/reset_password', methods=['POST'])
def reset_password():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No input data provided'}), 400

    token = data.get('token')
    user = users_collection.find_one({'reset_password_token': token})
    if not user:
        return jsonify({'message': 'Invalid token'}), 400

    password = data.get('password')
    password_hashed = hashlib.sha256(password.encode("utf-8")).hexdigest()
    users_collection.update_one({'_id': user['_id']}, {'$set': {'password': password_hashed, 'reset_password_token': None}})

    return jsonify({'message': 'Password reset successfully'}), 200


# def send_email_confirmation(email):
#     # Envoi d'un e-mail de confirmation
#     msg = MIMEText('Welcome to MyApp')
#     msg['Subject'] = 'Welcome to Animaixpert'
#     msg['From'] = 'sebasdeloco@gmail.com'
#     msg['To'] = email
#     #msg.body = 'Thank you for registering with MyApp!'
#     smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
#     smtp_server.login("sebasdeloco@gmail.com", "SEBASdeloco12")
#     smtp_server.sendmail("sebasdeloco@gmail.com", email, msg.as_string)
#     smtp_server.quit()
#     #mail.send(msg)

#     return jsonify({'message': 'User registered successfully'}), 201




if __name__ == '__main__':
    app.run(debug=True)