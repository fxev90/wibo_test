from typing import List
from pydantic import BaseModel
from bson import ObjectId

class CatBase(BaseModel):
    name: str
    breed: str
    age: int
    gender: str
    status: str
    description: str

class CatCreate(CatBase):
    pass

class Cat(CatBase):
    _id: ObjectId

    class Config:
        arbitrary_types_allowed = True

class CatResponse(CatBase):
    id: str