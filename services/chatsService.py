from models.chatModels import chats, chats_pydantic, chats_pydanticIN
from models.userModels import users
from models.type_nnModels import type_nn


async def get_all_chats():
    response = await chats.filter().prefetch_related('user', 'type_nn')
    response_data = []
    for chat in response:
        chat_data = {
            "id": chat.id,
            "chat_name": chat.chat_name,
            "date_creating": chat.date_creating,
            "date_deleting": chat.date_deleting,
            "deleting": chat.deleting,
            "user_id": chat.user.id,
            "type_nn_id": chat.type_nn.id
        }
        response_data.append(chat_data)
    return response_data


async def get_chat(chats_id: int):
    response = await chats.filter(id = chats_id).prefetch_related('user', 'type_nn')
    if response:
        response_data = []
        for chat in response:
            chat_data = {
                "id": chat.id,
                "chat_name": chat.chat_name,
                "date_creating": chat.date_creating,
                "date_deleting": chat.date_deleting,
                "deleting": chat.deleting,
                "user_id": chat.user.id,
                "type_nn_id": chat.type_nn.id
            }
            response_data.append(chat_data)
            print(response_data)
        return response_data
    else:
        return "Чат не найден"


async def get_chats_user_id(user_id: int):
    response = await chats.filter(user_id = user_id).prefetch_related('user', 'type_nn')
    if response:
        response_data = []
        for chat in response:
            chat_data = {
                "id": chat.id,
                "chat_name": chat.chat_name,
                "date_creating": chat.date_creating,
                "date_deleting": chat.date_deleting,
                "deleting": chat.deleting,
                "user_id": chat.user.id,
                "type_nn_id": chat.type_nn.id
            }
            response_data.append(chat_data)
        return response_data
    else:
        return "Не найден"


async def post_chat(user_id: int, type_nn_id: int, chat_info: chats_pydanticIN):    # type: ignore
    user_fk = await users.get(id = user_id)
    type_nn_fk = await type_nn.get(id = type_nn_id)
    chat_info = chat_info.dict(exclude_unset=True)
    chats_obj = await chats.create(**chat_info, user = user_fk, type_nn = type_nn_fk)
    return await chats_pydantic.from_tortoise_orm(chats_obj)


async def put_chat(chats_id: int, update_info: chats_pydanticIN):   # type: ignore
    chat = await chats.get(id = chats_id)
    update_info = update_info.dict(exclude_unset=True)
    chat.chat_name = update_info['chat_name']
    chat.date_creating = update_info['date_creating']
    if(update_info['date_deleting'] is not None): 
        chat.date_deleting = update_info['date_deleting']
    else: chat.date_deleting = None
    chat.deleting = update_info['deleting']
    await chat.save()
    return await chats_pydantic.from_tortoise_orm(chat)


async def del_chat(chats_id: int):
    return await chats.get(id=chats_id).delete()
