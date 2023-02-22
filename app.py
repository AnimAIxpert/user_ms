from flask import Flask
from pymongo import MongoClient
import os
from dotenv import load_dotenv


app = Flask(__name__)
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


if __name__ == '__main__':
	app.run(debug=True)