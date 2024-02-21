""" Module for storing API dependencies. """

import os

import jwt
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv

from api.models import Users, user_pydantic

load_dotenv()
JWT_SECRET = os.getenv("JWT_KEY")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Function to retrive current user based on token."""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        user = await Users.get(id=payload.get("id"))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password!",
        ) from e
    return await user_pydantic.from_tortoise_orm(user)
