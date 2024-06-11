from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from models.userModels import users, user_pydantic, user_pydanticIN

import jwt
from datetime import date


JWT_Secret = 'mysecret'
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')
invalidated_tokens = set()

async def authenticate_user(username: str, password: str):
    user = await users.get(email_user=username)
    if not user: 
        return False
    if not user.verify_password(password):
        return False
    return user

async def get_user_current(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, JWT_Secret, algorithms=['HS256'])
        user = await users.get(id = payload.get('id'))
    except: 
        raise HTTPException(status_code=401, detail="Неверная электронная почта или пароль")
    return await user_pydantic.from_tortoise_orm(user)   


async def generate_tokens(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        return{'error' : 'invalid authenticate'}
    
    user_obj = await user_pydantic.from_tortoise_orm(user)
    user_dict = user_obj.dict()
    
    for key, value in user_dict.items():
        if isinstance(value, date):
            user_dict[key] = value.isoformat()

    token = jwt.encode(user_dict, JWT_Secret)
    return  token

async def get_user(user: user_pydantic = Depends(get_user_current)): # type: ignore
    return user


async def logout(token: str = Depends(oauth2_scheme)):
    invalidated_tokens.remove(token)
    return "Выход выполнен успешно"