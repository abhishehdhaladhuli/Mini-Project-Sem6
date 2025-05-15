import firebase_admin
from firebase_admin import credentials, auth
from pymongo import MongoClient
from datetime import datetime

# Initialize Firebase Admin SDK
cred = credentials.Certificate("REPLACE_WITH_ACTUAL_JSON_FILE") #Replace with actual JSON File
firebase_admin.initialize_app(cred)

# MongoDB connection
mongo_uri = "mongodb+srv://<user>:<password>@cluster0.ciake.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(mongo_uri)
db = client["CampusConnect"]
users = db["users"]

# Function to sync Firebase user to MongoDB
def sync_user_to_db(uid):
    user_record = auth.get_user(uid)
    user_data = {
        "uid": user_record.uid,
        "name": user_record.display_name,
        "email": user_record.email,
        "provider": user_record.provider_data[0].provider_id if user_record.provider_data else "unknown",
        "createdAt": datetime.utcnow()
    }
    users.update_one({"uid": user_record.uid}, {"$set": user_data}, upsert=True)
    print("✅ Synced user to MongoDB")

# Example usage
sync_user_to_db("Replace with actual Firebase UID of a signed-in user")  # 🔁 Replace with actual Firebase UID of a signed-in user
