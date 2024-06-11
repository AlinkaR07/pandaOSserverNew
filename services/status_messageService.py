from models.status_messageModels import status_message, status_message_pydantic

async def get_all_status():
    return await status_message_pydantic.from_queryset(status_message.all())
    

async def get_status_message(status_message_id: int):
    return await status_message_pydantic.from_queryset_single(status_message.get(id = status_message_id))
    