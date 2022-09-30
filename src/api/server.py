""" Module handling REST API server.

REST API implementation on top of evolve package.
"""

# standard imports
import datetime
from datetime import timezone

# third-party imports
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise
from passlib.hash import bcrypt
import jwt

# internal imports
import models


JWT_SECRET = 'Kapil'

app = FastAPI(title="EVOLVE API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

async def autheticate_user(username: str, password: str):
    user = await models.Users.get(username=username)
    if user and user.verify_password(password):
        return user
    return False

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        user = await models.Users.get(id=payload.get('id'))
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid username or password!")
    return await models.user_pydantic.from_tortoise_orm(user)

@app.post('/token')
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await autheticate_user(form_data.username, form_data.password)
    if not user:
        return {"error": "invalid credentials"}
    user_obj = await models.user_token_pydantic.from_tortoise_orm(user)
    user_obj_json = user_obj.dict()
    user_obj_json.update({
        "exp": datetime.datetime.now(tz=timezone.utc) + datetime.timedelta(seconds=3600)
    })
    token = jwt.encode(user_obj_json, JWT_SECRET)
    return {'access_token': token, 'token_type': 'bearer'}

@app.post('/users', response_model=models.user_pydantic)
async def create_user(user: models.userin_pydantic):
    user_obj = models.Users(
        username=user.username,
        hashed_password = bcrypt.hash(user.hashed_password),
        email=user.email
    )
    await user_obj.save()
    return await models.user_pydantic.from_tortoise_orm(user_obj)

@app.get('/users', response_model=models.user_pydantic)
async def get_user(user: models.user_pydantic = Depends(get_current_user)):
    return user


register_tortoise(
    app,
    db_url='sqlite://db.sqlite3',
    modules={'models': ['models']},
    generate_schemas=True,
    add_exception_handlers=True
)
