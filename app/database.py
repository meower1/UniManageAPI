"""
Mongodb configuration settings
"""

from pymongo import MongoClient

# MongoDB connection URL
# MONGO_URL = "mongodb://localhost:27017"
MONGO_URL = "mongodb://mongo:27017"
client = MongoClient(MONGO_URL)
database = client["lorestanuniv"]
course_collection = database["course"]
lecturer_collection = database["lecturer"]
student_collection = database["student"]
presentedcourses_collection = database["presentedcourses"]
courseregister_collection = database["courseregister"]
