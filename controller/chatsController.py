from fastapi import APIRouter
from models.chatModels import chats_pydanticIN

from services.chatsService import get_all_chats, get_chat, get_chats_user_id, post_chat, put_chat, del_chat

router = APIRouter()

@router.get("/chats", tags=["Chats"])
async def get_all_chat():
    response = await get_all_chats()
    return {"status": "ok", "data": response}


@router.get("/chats/{chats_id}", tags=["Chats"])
async def get_chat_id(chats_id: int):
    response = await get_chat(chats_id)
    if (response == "Чат не найден не найден"): 
        return {"status": "error", "data": response}
    else:
        return {"status": "ok", "data": response}


@router.get("/chats/user/{user_id}", tags=["Chats"])
async def get_chats_by_user_id(user_id: int):
    response = await get_chats_user_id(user_id)
    if (response == "Не найден"): 
        return {"status": "error", "data": response}
    else:
        return {"status": "ok", "data": response}



@router.post("/chats/{user_id}/{type_nn_id}", tags=["Chats"])
async def create_chat(user_id: int, type_nn_id: int, chat_info: chats_pydanticIN): # type: ignore
    response = await post_chat(user_id, type_nn_id, chat_info)
    return {"status": "ok", "data" : response}


@router.put("/chats/{chats_id}", tags=["Chats"])
async def update_chat(chats_id: int, update_info: chats_pydanticIN): # type: ignore
    response = await put_chat(chats_id, update_info)
    return {"status": "ok", "data" : response}


@router.delete("/chats/{chats_id}", tags=["Chats"])
async def delete_chat(chats_id: int):
    await del_chat(chats_id)
    return {"status": "ok"}
