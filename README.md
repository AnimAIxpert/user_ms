# user_ms
AnimAIxpert's User Microservice

To install dependencies:

pip install -r requirements.txt


To run:

flask --app app run

or

python -m flask --app app run

Create user in mongodb:

use admin

db.createUser({
    user: "animaixpert",
    pwd: passwordPrompt(),
    roles: [ { role: "userAdminAnyDatabase", db: "admin" }, "readWriteAnyDatabase" ]
    }
)

create .env file with the following environment variables:

MONGO_USERNAME
MONGO_PORT
MONGO_PASSWORD
MONGO_DATABASE
MONGO_HOST