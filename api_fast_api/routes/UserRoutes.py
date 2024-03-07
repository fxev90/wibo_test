from fastapi import APIRouter, HTTPException, Path, status, Response, Query, Depends
from models.User import User, UserDB, UserRegister, UserResponse
from config.db import get_mongo_client
from bson import ObjectId
from passlib.context import CryptContext
from dotenv import load_dotenv
import os
from schemas.UserSchemas import userSchema, usersSchema
from pymongo import IndexModel, ASCENDING, errors
from auth.jwt import get_current_user

load_dotenv()

PASSWORD_HASH_ALGORITHM = "bcrypt"
password_context = CryptContext(schemes=[PASSWORD_HASH_ALGORITHM], deprecated="auto")

user_router = APIRouter()
db = get_mongo_client()
email_username_index = IndexModel([('email', ASCENDING), ('username', ASCENDING)], unique=True)
db.users.create_indexes([email_username_index])

@user_router.get("/user/", response_model=list[UserResponse], tags=["users"])
async def find_all_users(skip: int = Query(0, alias="page", ge=1), limit: int = Query(10, le=100), name: str = None, email: str = None, current_user: str = Depends(get_current_user)):
    """
    A function to find all users with optional filtering by name and email, and pagination.
    
    Parameters:
        skip: int = Query(0, alias="page", ge=1) - the number of records to skip for pagination
        limit: int = Query(10, le=100) - the maximum number of records to retrieve
        name: str = None - optional parameter for filtering by name
        email: str = None - optional parameter for filtering by email
        current_user: str = Depends(get_current_user) - the current user making the request
    
    Returns:
        list[UserResponse] - a list of user responses
    """
    # Define query parameters for filtering
    filters = {}
    if name:
        filters["name"] = name
    if email:
        filters["email"] = email

    # Apply pagination and filters to the MongoDB query
    users_cursor = db.users.find(filters).skip((skip - 1) * limit).limit(limit)

    # Return the paginated and filtered results
    return usersSchema(users_cursor)

@user_router.post("/user/", response_model=UserResponse, tags=["users"])
async def create_user(user: UserRegister):
    """
    A function to create a new user in the database.

    Args:
        user: UserRegister - The user information to be registered.

    Returns:
        UserResponse: The response containing the newly created user data.

    Raises:
        HTTPException: If there is a duplicate key error (email or username already exists) or if there is an unknown error.
    """
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

@user_router.get("/user/{user_id}", response_model=UserResponse, tags=["users"])
async def read_user(user_id: str = Path(..., description="User ID"), current_user: str = Depends(get_current_user)):
    """
    A function to read user data based on the user ID and return the user data response.
    
    Parameters:
    - user_id: str = Path(..., description="User ID")
    - current_user: str = Depends(get_current_user)
    
    Returns:
    - UserResponse: The response model for the user data.
    """
    try:
        user_db = db.users.find_one({"_id": ObjectId(user_id)})
        if user_db:
            user_data_response = userSchema(user_db)
            return user_data_response
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@user_router.put("/user/{user_id}", response_model=UserResponse, tags=["users"])
async def update_user(user: UserRegister,user_id: str = Path(..., description="User ID"), current_user: str = Depends(get_current_user)):
    """
    Update user information in the database and return the updated user data.

    Parameters:
    - user: UserRegister model object containing the user information to be updated
    - user_id: str, the ID of the user to be updated
    - current_user: str, the current user making the update request

    Returns:
    - UserResponse model object containing the updated user data
    - HTTPException with status code 404 if the user is not found
    - HTTPException with status code 500 if an unexpected error occurs
    """
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

@user_router.delete("/user/{user_id}",  tags=["users"])
async def delete_user(user_id: str = Path(..., description="User ID"), current_user: str = Depends(get_current_user)):
    """
    A function to delete a user by user ID, with authentication and error handling.
    """
    try:
        db.users.find_one_and_delete({"_id": ObjectId(user_id)})

        return Response(status_code= status.HTTP_204_NO_CONTENT)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    pass