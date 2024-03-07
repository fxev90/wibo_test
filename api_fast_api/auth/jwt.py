# auth.py

from fastapi import HTTPException, status, Depends
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
import os

load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
PASSWORD_HASH_ALGORITHM ="bcrypt"
password_context = CryptContext(schemes=[PASSWORD_HASH_ALGORITHM], deprecated="auto")


def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Returns the current user based on the provided token.

    Parameters:
    - token (str): the authentication token

    Returns:
    - str: the username of the current user
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    return username

