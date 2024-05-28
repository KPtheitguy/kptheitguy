from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from datetime import datetime
import jwt  

from app.config import ACTIVE_DB, DB_CONFIG, JWT_SECRET_KEY, JWT_ALGORITHM

router = APIRouter()

if ACTIVE_DB == "mongodb":
    client = MongoClient(DB_CONFIG["uri"])
    db = client[DB_CONFIG["database_name"]]
    users_collection = db[DB_CONFIG["collection_name"]]

class CreateUserRequest(BaseModel):
    first_name: str
    last_name: str
    username: str
    password: str
    email: str
    phone_number: str
    token: str  

@router.post("/users/create")
async def create_user(user: CreateUserRequest):
    try:
        payload = jwt.decode(user.token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        username = payload.get("sub")

        # Check if the user already exists
        existing_user = users_collection.find_one({"username": user.username})
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already taken")

        # Create a new user
        new_user = {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
            "password": user.password,  
            "email": user.email,
            "phone_number": user.phone_number,
            "token": None,
            "token_expiry": None
        }
        users_collection.insert_one(new_user)
        return {"message": "User created successfully"}

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")

    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
