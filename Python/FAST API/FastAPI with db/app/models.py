from pydantic import BaseModel, Field
from datetime import datetime
from sqlmodel import SQLModel, Field as SQLField

class User(BaseModel):
    username: str = Field(...)
    password: str = Field(...)
    token: str = Field(None)
    token_expiry: datetime = Field(None)

class UserSQL(SQLModel, table=True):
    id: int = SQLField(default=None, primary_key=True)
    username: str
    password: str
    token: str = None
    token_expiry: datetime = None
