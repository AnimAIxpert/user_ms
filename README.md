# user_ms
AnimAIxpert's User Microservice

To install dependencies:

pip install -r requirements.txt


To run:

flask --app app run


Create user in mongodb:

db.createUser({
    user: "animaixpert",
    pwd: passwordPrompt(),
    roles: [ { role: "userAdminAnyDatabase", db: "admin" }, "readWriteAnyDatabase" ]
    }
)