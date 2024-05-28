from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from pymongo import MongoClient
from datetime import datetime, timedelta
import jwt 
#import PyJWT
from sqlmodel import Session, select, SQLModel, create_engine

from app.models import User, UserSQL
from app.config import ACTIVE_DB, DB_CONFIG, JWT_SECRET_KEY, JWT_ALGORITHM, TOKEN_EXPIRY_HOURS

router = APIRouter()

if ACTIVE_DB == "mongodb":
    client = MongoClient(DB_CONFIG["uri"])
    db = client[DB_CONFIG["database_name"]]
    users_collection = db[DB_CONFIG["collection_name"]]

else:
    engine = create_engine(DB_CONFIG["connection_string"])
    SQLModel.metadata.create_all(engine)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/token")
async def get_token(login_request: LoginRequest):
    username = login_request.username
    password = login_request.password

    if ACTIVE_DB == "mongodb":
        user_data = users_collection.find_one({"username": username})
        if user_data and user_data['password'] == password:
            token = handle_token(user_data, username)
            return {"access_token": token, "token_type": "bearer"}

    else:
        with Session(engine) as session:
            statement = select(UserSQL).where(UserSQL.username == username)
            results = session.exec(statement)
            user_data = results.first()
            if user_data and user_data.password == password:
                token = handle_token(user_data, username, db_type='sqlmodel')
                return {"access_token": token, "token_type": "bearer"}

    raise HTTPException(status_code=400, detail="Incorrect username or password")

def handle_token(user_data, username, db_type='mongodb'):
    # Check if token exists and is still valid
    if db_type == 'mongodb':
        if user_data.get('token') and user_data.get('token_expiry'):
            token_expiry = user_data['token_expiry']
            if token_expiry > datetime.utcnow():
                return user_data['token']
    else:
        if user_data.token and user_data.token_expiry:
            token_expiry = user_data.token_expiry
            if token_expiry > datetime.utcnow():
                return user_data.token

    # Generate new token if no valid token exists
    token_data = {
        "sub": username,
        "exp": datetime.utcnow() + timedelta(hours=TOKEN_EXPIRY_HOURS)
    }
    token = jwt.encode(token_data, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

    if db_type == 'mongodb':
        users_collection.update_one(
            {"username": username},
            {"$set": {"token": token, "token_expiry": datetime.utcnow() + timedelta(hours=TOKEN_EXPIRY_HOURS)}}
        )
    else:
        with Session(engine) as session:
            user_data.token = token
            user_data.token_expiry = datetime.utcnow() + timedelta(hours=TOKEN_EXPIRY_HOURS)
            session.add(user_data)
            session.commit()

    return token

@router.get("/users/me")
async def read_users_me(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        username = payload.get("sub")

        if ACTIVE_DB == "mongodb":
            user_data = users_collection.find_one({"username": username})
            if user_data:
                return user_data

        else:
            with Session(engine) as session:
                statement = select(UserSQL).where(UserSQL.username == username)
                results = session.exec(statement)
                user_data = results.first()
                if user_data:
                    return user_data

        raise HTTPException(status_code=404, detail="User not found")

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")

    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
