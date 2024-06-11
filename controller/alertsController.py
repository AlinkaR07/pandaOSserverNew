from fastapi import APIRouter
from models.alertsModels import alerts_pydanticIN
from services.alertsService import get_all_alert, get_alert, post_alert, put_alert, del_alert


router = APIRouter()

@router.get("/alerts", tags=["Alerts"])
async def get_all_alerts():
    response = await get_all_alert()
    return {"status": "ok", "data": response}


@router.get("/alerts/{alerts_id}", tags=["Alerts"])
async def get_alert_id(alerts_id: int):
    response = await get_alert(alerts_id)
    if (response == "Оповещение не найдено"):
        return {"status": "error", "message": response}
    else:
        return {"status": "ok", "message": response}

@router.post("/alerts/{user_id}", tags=["Alerts"])
async def create_alert(user_id: int, alert_info: alerts_pydanticIN):   # type: ignore
    response = await post_alert(user_id, alert_info)
    return {"status": "ok", "data" : response}


@router.put("/alerts/{alerts_id}", tags=["Alerts"])
async def update_alert(alerts_id: int, update_info: alerts_pydanticIN):     # type: ignore
    response = await put_alert(alerts_id, update_info)
    return {"status": "ok", "data" : response}


@router.delete("/alerts/{alerts_id}", tags=["Alerts"])
async def delete_alert(alerts_id: int):
    await del_alert(alerts_id)
    return {"status": "ok"}
