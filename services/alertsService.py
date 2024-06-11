from models.alertsModels import alerts, alerts_pydantic, alerts_pydanticIN
from models.userModels import users

async def get_all_alert():
    response = await alerts.filter().prefetch_related('user')
    response_data = []
    for alert in response:
        alert_data = {
            "id": alert.id,
            "date_sending": alert.date_sending,
            "reading": alert.reading,
            "user_id": alert.user.id
        }
        response_data.append(alert_data)
    return response_data


async def get_alert(alerts_id: int):
    response = await alerts.filter(id = alerts_id).prefetch_related('user')
    if response:
        response_data = []
        for alert in response:
            alert_data = {
                "id": alert.id,
                "date_sending": alert.date_sending,
                "reading": alert.reading,
                "user_id": alert.user.id
            }
            response_data.append(alert_data)
            print(response_data)
        return response_data
    else:
        return "Оповещение не найдено"


async def post_alert(user_id: int, alert_info: alerts_pydanticIN): # type: ignore
    user_fk = await users.get(id = user_id)
    alert_info = alert_info.dict(exclude_unset=True)
    alerts_obj = await alerts.create(**alert_info, user = user_fk)
    return await alerts_pydantic.from_tortoise_orm(alerts_obj)
    

async def put_alert(alerts_id: int, update_info: alerts_pydanticIN): # type: ignore
    alert = await alerts.get(id = alerts_id)
    update_info = update_info.dict(exclude_unset=True)
    alert.reading = update_info['reading']
    await alert.save()
    return await alerts_pydantic.from_tortoise_orm(alert)


async def del_alert(alerts_id: int):
    return await alerts.get(id=alerts_id).delete()

