import os
from urllib.parse import quote_plus
from dotenv import load_dotenv

load_dotenv()

username = os.getenv("MONGO_USERNAME")
password = os.getenv("MONGO_PASSWORD")
host = os.getenv("MONGO_HOST")

password_enc = quote_plus(password)
username_enc = quote_plus(username)

MONGO_URI = f"mongodb+srv://{username_enc}:{password_enc}@{host}/?retryWrites=true&w=majority"

class Config:
    MONGO_URI = MONGO_URI
