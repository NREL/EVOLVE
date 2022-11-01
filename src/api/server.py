""" Module handling REST API server.

REST API implementation on top of evolve package.
"""

# standard imports
import datetime
from datetime import timezone
import os
from pathlib import Path

# third-party imports
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise
from passlib.hash import bcrypt
import jwt
from dotenv import load_dotenv


# internal imports
import models
from dependencies.dependency import get_current_user
from routes import (
    timeseries_data_routes, 
    timeseries_data_comment_routes,
    timeseries_data_sharing_routes
)

load_dotenv()
JWT_SECRET = os.getenv('JWT_KEY')
DATA_PATH = os.getenv('DATA_PATH')

app = FastAPI(title="EVOLVE API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(timeseries_data_routes.router)
app.include_router(timeseries_data_comment_routes.router)
app.include_router(timeseries_data_sharing_routes.router)

async def autheticate_user(username: str, password: str):
    user = await models.Users.get(username=username)
    if user and user.verify_password(password):
        return user
    return False


@app.get('/health')
async def get_health():
    return {"message": "healthy"}

@app.post('/token')
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await autheticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid username or password!")
            
    user_obj = await models.user_token_pydantic.from_tortoise_orm(user)
    user_obj_json = user_obj.dict()
    user_obj_json.update({
        "exp": datetime.datetime.now(tz=timezone.utc) + datetime.timedelta(seconds=3600)
    })
    token = jwt.encode(user_obj_json, JWT_SECRET)
    return {'access_token': token, 'token_type': 'bearer'}

@app.post('/users', response_model=models.user_pydantic)
async def create_user(user: models.userin_pydantic):
    """ Creates a user."""

    user_obj = models.Users(
        username=user.username,
        hashed_password = bcrypt.hash(user.hashed_password),
        email=user.email
    )
    await user_obj.save()
    return await models.user_pydantic.from_tortoise_orm(user_obj)

@app.get('/users', response_model=models.user_pydantic)
async def get_user(user: models.user_pydantic = Depends(get_current_user)):
    """ Gets user info. """
    return user


register_tortoise(
    app,
    db_url='sqlite://db.sqlite3',
    modules={'models': ['models']},
    generate_schemas=True,
    add_exception_handlers=True
)