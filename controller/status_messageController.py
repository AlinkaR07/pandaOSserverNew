from fastapi import APIRouter

from models.status_messageModels import status_message_pydantic, status_message
from services.status_messageService import get_all_status, get_status_message

router = APIRouter()

@router.get("/status_message", tags=["Status_message"])
async def get_all_status_message():
    response = await get_all_status()
    return {"status": "ok", "data" : response}


@router.get("/status_message/{status_message_id}", tags=["Status_message"])
async def get_status_message_id(status_message_id: int):
    response = await get_status_message(status_message_id)
    return {"status": "ok", "data" : response}
