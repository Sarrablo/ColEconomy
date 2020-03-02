from pymongo import MongoClient
from bson.objectid import ObjectId

class MongoModel():
    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.database = self.client.bunuel

    def find_by_user(self, user):
        user = self.database.users.find_one({"user": user})
        return user

    def compare_by_pass(self, user, password):
        data = self.find_by_user(user)
        if data is not None:
            if data.get("password", "") == password:
                return True
            else:
                return False

    def insert_in_operations(self, data):
        return self.database.operations.insert_one(data).inserted_id

    def delete_operations(self, identifier, who):
        return self.database.operations.update_one(
            {"_id": ObjectId(identifier)}, {"$set": {
                "deleted": True,
                "deleter": who
            }})

    def find_operations(self):
        return list(
            self.database.operations.find({
                "deleted": {
                    "$ne": True
                }
            }).sort("_id", -1))
