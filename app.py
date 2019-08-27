from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = "secret key"
# app.config["MONGO_URI"]="mongodb://localhost:27017/dbsong"
mongo = MongoClient('mongodb://localhost:27017')['dbsong']