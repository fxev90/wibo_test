from fastapi import APIRouter, HTTPException, Path, status, Response, Query, Depends
from config.db import get_mongo_client
from bson import ObjectId
from passlib.context import CryptContext
from dotenv import load_dotenv
import os
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from auth.jwt import get_current_user

db = get_mongo_client()
auth_router = APIRouter()

load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
PASSWORD_HASH_ALGORITHM ="bcrypt"
password_context = CryptContext(schemes=[PASSWORD_HASH_ALGORITHM], deprecated="auto")


@auth_router.post("/login/", tags = ["auth"])
def login(username: str, password: str):
    user = db.users.find_one({"username": username})
    if not user or not password_context.verify(password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token_data = {"sub": username, "id": str(user["_id"])}
    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}


@auth_router.get("/protected", tags = ["auth"])
def protected_route(current_user: str = Depends(get_current_user)):
    return {"message": f"Hello {current_user}, you are authenticated!"}