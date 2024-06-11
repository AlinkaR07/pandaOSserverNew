from fastapi import APIRouter

from models.userModels import user_pydanticIN
from services.usersService import get_all_users, get_user_id, get_user_email, post_user, put_user, del_user

router = APIRouter()


@router.get("/user", tags=["Users"])
async def get_all_user():
    response = await get_all_users()
    return {"status": "ok", "data" : response}


@router.get("/user/{user_id}", tags=["Users"])
async def get_user(user_id: int):
    response = await get_user_id(user_id)
    return {"status": "ok", "data" : response}


@router.get("/user_email/{user_email}", tags=["Users"])
async def get_user(user_email: str):
    response = await get_user_email(user_email)
    return {"status": "ok", "data" : response}


@router.post("/user", tags=["Users"])
async def create_user(user_info: user_pydanticIN):  # type: ignore
    response = await post_user(user_info)
    return {"status": "ok", "data" : response}


@router.put("/user/{user_id}", tags=["Users"])
async def update_user(user_id: int, update_info: user_pydanticIN): # type: ignore
    response = await put_user(user_id, update_info)
    return {"status": "ok", "data" : response}


@router.delete("/user/{user_id}", tags=["Users"])
async def delete_user(user_id: int):
    await del_user(user_id)
    return {"status": "ok"}
