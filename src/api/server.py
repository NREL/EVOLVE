""" Module handling REST API server.

REST API implementation on top of evolve package.
"""

# standard imports
import datetime
from datetime import timezone
from typing import List
import os
from pathlib import Path

# third-party imports
from fastapi import FastAPI, HTTPException, Depends, status, File, Form, BackgroundTasks
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise
from passlib.hash import bcrypt
import jwt
from dotenv import load_dotenv

# internal imports
import models
import timeseries_data
import custom_models


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


@app.post('/data/upload', response_model=List[models.ts_minimal])
async def upload_timeseries_data(
    # background_tasks: BackgroundTasks,
    file: bytes = File(),
    metadata: str = Form(),
    user: models.user_pydantic = Depends(get_current_user),
):

    metadata_pydantic = timeseries_data.TSFormInput.parse_raw(metadata)
    response = await timeseries_data.handle_timeseries_data_upload(
        file, metadata_pydantic, user
    )
    if response:
        # for ts_data in response:
        #     background_tasks.add_task(timeseries_data.create_ts_image, ts_data.filename, ts_data.name)
        return response

    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Bad input data or validation failed!"
        )

@app.get('/data', response_model=List[models.ts_pydantic])
async def get_timeseries_data(user: models.user_pydantic = Depends(get_current_user)):
    
    ts_data = await models.TimeseriesData.all().filter(username=user.username)
    if not ts_data:
        ts_data = []
    if not isinstance(ts_data, list):
        ts_data = [ts_data]
    ts_data_pydantic = [await models.ts_pydantic.from_tortoise_orm(data) for data in ts_data]
    return ts_data_pydantic

@app.delete('/data/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_ts_data(id: int, user: models.user_pydantic = Depends(get_current_user)):

    ts_data = await models.TimeseriesData.get(id=id, username=user.username)
    file_name = ts_data.filename + '.csv'
    file_path = Path(DATA_PATH) / user.username / 'timeseries_data' / file_name
    await ts_data.delete()
    file_path.unlink(missing_ok=True)

    return 

@app.get('/data/{id}/file')
async def get_data_for_download(id:int, user: models.user_pydantic = Depends(get_current_user)):
    
    ts_data = await models.TimeseriesData.get(id=id, username=user.username)
    file_name = ts_data.filename + '.csv'
    file_path = Path(DATA_PATH) / user.username / 'timeseries_data' / file_name
    return FileResponse(file_path)


@app.post('/data/{data_id}/comments', response_model=models.data_comments_pydantic)
async def create_data_comment(
    comment: custom_models.DataCommentInput,
    data_id: int,
    user: models.user_pydantic = Depends(get_current_user)):
    
    comment_obj = models.DataComments(
        data_id = data_id,
        username = user.username,
        comment=comment.comment,
        edited=False
    )
    await comment_obj.save()
    return await models.data_comments_pydantic.from_tortoise_orm(comment_obj)

@app.get('/data/{data_id}/comments', response_model=List[models.data_comments_pydantic])
async def get_comments_for_data(data_id:int, user: models.user_pydantic = Depends(get_current_user)):
    
    comments = await models.DataComments.all().filter(data_id=data_id)
    return [await models.data_comments_pydantic.from_tortoise_orm(comment) \
        for comment in comments]

@app.delete('/data/{data_id}/comments/{comment_id}', status_code=status.HTTP_204_NO_CONTENT)
async def get_comments_for_data(
    data_id:int, 
    comment_id: int,
    user: models.user_pydantic = Depends(get_current_user)):
    
    comment = await models.DataComments.get(data_id=data_id, 
        id=comment_id, username=user.username)
    await comment.delete()

@app.put('/data/{data_id}/comments/{comment_id}', response_model=models.data_comments_pydantic)
async def get_comments_for_data(
    data_id:int, 
    comment_id: int,
    updated_comment: custom_models.DataCommentInput,
    user: models.user_pydantic = Depends(get_current_user)):
    
    comment = await models.DataComments.get(data_id=data_id, 
        id=comment_id, username=user.username)
    comment.comment = updated_comment.comment
    comment.edited = True
    await comment.save()
    return await models.data_comments_pydantic.from_tortoise_orm(comment)
    


register_tortoise(
    app,
    db_url='sqlite://db.sqlite3',
    modules={'models': ['models']},
    generate_schemas=True,
    add_exception_handlers=True
)
