from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017")


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"