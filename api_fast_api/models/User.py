from pydantic import BaseModel
from bson import ObjectId

# Pydantic model for User
class User(BaseModel):
    name: str
    username: str
    email: str
    
class UserRegister(User):
    password: str

# MongoDB document model for User
class UserDB(User):
    id: ObjectId
    
    class Config:
        arbitrary_types_allowed = True
        
class UserResponse(User):
    id: str
