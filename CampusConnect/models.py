from pydantic import BaseModel

class User(BaseModel):
    name: str
    email: str
    role: str = "student"
    college: str
