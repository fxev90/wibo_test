from fastapi import APIRouter, HTTPException, Path, status, Response, Query
from models.User import User, UserDB, UserRegister, UserResponse
from config.db import get_mongo_client
from bson import ObjectId
from passlib.context import CryptContext
from dotenv import load_dotenv
import os
from schemas.UserSchemas import userSchema, usersSchema
from pymongo import IndexModel, ASCENDING, errors

load_dotenv()

PASSWORD_HASH_ALGORITHM = "bcrypt"
password_context = CryptContext(schemes=[PASSWORD_HASH_ALGORITHM], deprecated="auto")

userRouter = APIRouter()
db = get_mongo_client()
email_username_index = IndexModel([('email', ASCENDING), ('username', ASCENDING)], unique=True)
db.users.create_indexes([email_username_index])

@userRouter.get("/user/", response_model=list[UserResponse], tags=["users"])
async def find_all_users(skip: int = Query(0, alias="page", ge=0), limit: int = Query(10, le=100), name: str = None, email: str = None):
    # Define query parameters for filtering
    filters = {}
    if name:
        filters["name"] = name
    if email:
        filters["email"] = email

    # Apply pagination and filters to the MongoDB query
    users_cursor = db.users.find(filters).skip(skip).limit(limit)

    # Return the paginated and filtered results
    return usersSchema(users_cursor)

@userRouter.post("/user/", response_model=UserResponse, tags=["users"])
async def create_user(user: UserRegister):
    try:
        new_user = user.dict()
        new_user["password"] = password_context.hash(new_user["password"])
        user_db = db.users.insert_one(new_user)
        user_db = db.users.find_one({"_id": user_db.inserted_id})
        user_data_response = userSchema(user_db)
        return user_data_response
    except errors.DuplicateKeyError:
        # Handle duplicate key error (email or username already exists)
        raise HTTPException(status_code=400, detail="Email or username already registered")
    except Exception as e:
        # Handle other exceptions
        raise HTTPException(status_code=500, detail=str('Unknown error'))

@userRouter.get("/user/{user_id}", response_model=UserResponse, tags=["users"])
async def read_user(user_id: str = Path(..., description="User ID")):
    try:
        user_db = db.users.find_one({"_id": ObjectId(user_id)})
        if user_db:
            user_data_response = userSchema(user_db)
            return user_data_response
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@userRouter.put("/user/{user_id}", response_model=UserResponse, tags=["users"])
async def update_user(user: UserRegister,user_id: str = Path(..., description="User ID")):
    try:
        new_user = user.dict()
        new_user["password"] = password_context.hash(new_user["password"])
        user_db = db.users.find_one_and_update({"_id": ObjectId(user_id)}, {"$set": new_user})
        if user_db:
            user_data_response = userSchema(user_db)
            return user_data_response
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@userRouter.delete("/user/{user_id}",  tags=["users"])
async def delete_user(user_id: str = Path(..., description="User ID")):
    try:
        db.users.find_one_and_delete({"_id": ObjectId(user_id)})

        return Response(status_code= status.HTTP_204_NO_CONTENT)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    pass