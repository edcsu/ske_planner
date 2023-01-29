from typing import Optional, List
from beanie import Document, Link

from pydantic import BaseModel, EmailStr

from models.events import Event

class User(Document):
    email: EmailStr
    password: str
    events: Optional[List[Link[Event]]]
    class Settings:
        name = "users"
    class Config:
        schema_extra = {
            "example": {
                "email": "fastapi@gmail.com",
                "password": "strong!!!",
                "events": [],
            } 
        }
        
class UserSignIn(BaseModel):
    email: EmailStr
    password: str

class NewUser(User):
    password: str

    class Config:
        schema_extra = {
            "example": {
                "email": "fastapi@packt.com",
                "password": "Stro0ng!",
                "username": "FastPackt"
            }
        }