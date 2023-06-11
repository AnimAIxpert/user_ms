# user_ms
AnimAIxpert's User Microservice

To install dependencies:

pip install -r requirements.txt


To run:


flask --app app run

or

python3 -m flask --app app run

Create user in mongodb:
(si on utilise le docker)=> docker exec -it eb8 mongosh -u root -p

use admin

db.createUser({
    user: "animaixpert",
    pwd: passwordPrompt(),
    roles: [ { role: "userAdminAnyDatabase", db: "admin" }, "readWriteAnyDatabase" ]
    }
)

db.updateUser("animaixpert",{
pwd: passwordPrompt(),
roles: [ { role: "userAdminAnyDatabase", db: "admin" }, "readWriteAnyDatabase" ]
}
)

enable authentication in mongo:

test mongosh authentication

mongosh -u animaixpert -p --authenticationDatabase admin

create .env file with the following environment variables:

MONGO_USERNAME
MONGO_PORT
MONGO_PASSWORD
MONGO_DATABASE
MONGO_HOST

if you are using Windows add also:

FLASK_APP = server.py
FLASK_ENV = development
FLASK_RUN_PORT = 8000

"date_added": "2014-01-22T14:56:59.301Z"
pm.collectionVariables.set("token", pm.response.json()["access_token"]);


Configuration des images du docker 
docker build -t animaixpert/user_ms .   (on doit tjrs la faire après chaque modification de code )
docker images
docker run animaixpert/user_ms 

lancer le container docker / mongo
on a créer le fichier animaixpert.yml
docker-compose -f animaixpert.yml up
