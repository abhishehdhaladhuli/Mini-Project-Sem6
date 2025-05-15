from pymongo import MongoClient
from datetime import datetime

# ✅ MongoDB Atlas connection
uri = "mongodb+srv://<user>:<password>@cluster0.ciake.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)
db = client["CampusConnect"]

# ✅ Collections
users = db["users"]
posts = db["posts"]
comments = db["comments"]
notes = db["notes"]
internships = db["internships"]
applications = db["applications"]
chat_rooms = db["chat_rooms"]
messages = db["messages"]
items = db["items"]
notifications = db["notifications"]

# ✅ Clear previous data if needed
users.delete_many({})
posts.delete_many({})
comments.delete_many({})
notes.delete_many({})
internships.delete_many({})
applications.delete_many({})
chat_rooms.delete_many({})
messages.delete_many({})
items.delete_many({})
notifications.delete_many({})

# ✅ Indexes for performance and filtering
users.create_index("email", unique=True)
posts.create_index("user_id")
posts.create_index([("content", "text"), ("tags", "text")])
comments.create_index("post_id")
notes.create_index([("subject", 1), ("tags", 1)])
internships.create_index("domain")
applications.create_index([("user_id", 1), ("internship_id", 1)])
chat_rooms.create_index("participants")
messages.create_index("chat_room_id")
items.create_index("owner_id")
notifications.create_index("user_id")

print("✅ CampusConnect setup complete! Collections created and indexes initialized.")
