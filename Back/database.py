from pymongo import MongoClient

MONGO_URI = "mongodb+srv://Proyecto:12345@cluster0.paotbxz.mongodb.net/mathlite?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(MONGO_URI)

db = client["mathlite"]

executions = db["executions"]