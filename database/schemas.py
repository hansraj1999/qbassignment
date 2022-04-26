from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum


class Student(BaseModel):
    name: str | None = None
    email: str
    password: str | None = None
    president_voted_for: str | None = None
    vice_president_for: str | None = None

    class Config:
        orm_mode = True


class President(BaseModel):
    id : int
    name: str
    total_votes: int


class VicePresident(BaseModel):
    id : str
    name: str
    total_votes: int


class Choice(str, Enum):
    President = "President"
    Vice_President = 'Vice President'


class TokenData(BaseModel):
    name: Optional[str] = None
