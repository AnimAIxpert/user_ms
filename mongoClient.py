from pymongo import MongoClient
from dotenv import load_dotenv
import os
load_dotenv()


MONGO_HOST = os.environ.get('MONGO_HOST')
MONGO_PORT = int(os.environ.get('MONGO_PORT'))
MONGO_USERNAME = os.environ.get('MONGO_USERNAME')
MONGO_PASSWORD = os.environ.get('MONGO_PASSWORD')

# print("MONGO_HOST: ", MONGO_HOST)
# print("MONGO_PORT: ", MONGO_PORT)
# print("MONGO_USERNAME: ", MONGO_USERNAME)
# print("MONGO_PASSWORD: ", MONGO_PASSWORD)

client = MongoClient(f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}")

# print(client.server_info())