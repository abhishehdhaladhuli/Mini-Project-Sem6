from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from models import User
from db import db
from firebase_user_sync import sync_user_to_db  # ✅ Import the sync function

app = FastAPI()

# Allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/users")
def add_user(user: User):
    db["users"].insert_one(user.dict())
    return {"message": "User added successfully"}

@app.get("/users")
def get_users():
    return list(db["users"].find({}, {"_id": 0}))

# ✅ NEW Firebase UID sync route
@app.post("/firebase-sync")
async def firebase_sync(request: Request):
    data = await request.json()
    uid = data.get("uid")
    if not uid:
        return {"error": "UID not provided"}

    try:
        sync_user_to_db(uid)
        return {"message": f"✅ User with UID {uid} synced successfully"}
    except Exception as e:
        return {"error": str(e)}
