from typing import List
from pydantic import BaseModel, ObjectId

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
    id: ObjectId

    class Config:
        arbitrary_types_allowed = True
        odm_mode = True