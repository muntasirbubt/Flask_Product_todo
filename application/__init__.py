from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["SECRET_KEY"]= "59ffe9ca100e0d560d55ca06f4928d4dab88757e"
app.config["MONGO_URI"] = "mongodb://localhost:27017/myFirstDB"

#setup mongodb

mongodb_client = PyMongo(app)
db = mongodb_client.db


from application import routes 