from pydantic import BaseModel

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