from passlib.hash import bcrypt

from models.userModels import users, user_pydantic, user_pydanticIN


async def get_all_users():
    return await user_pydantic.from_queryset(users.all())


async def get_user_id(user_id: int):
    return await user_pydantic.from_queryset_single(users.get(id = user_id))


async def get_user_email(user_email: str):
    return await user_pydantic.from_queryset_single(users.get(email_user = user_email))


async def post_user(user_info: user_pydanticIN):  # type: ignore
    bcrypt_password = None
    if user_info.password is not None:
        bcrypt_password = bcrypt.hash(user_info.password)
    user_obj = await users.create(name_user=user_info.name_user, 
                                  email_user=user_info.email_user, 
                                  photo=user_info.photo, 
                                  date_registration=user_info.date_registration, 
                                  date_lastAuth=user_info.date_lastAuth, 
                                  status=user_info.status, 
                                  bloking=user_info.bloking, 
                                  confirmed=user_info.confirmed, 
                                  password=bcrypt_password)
    return await user_pydantic.from_tortoise_orm(user_obj)


async def put_user(user_id: int, update_info: user_pydanticIN): # type: ignore
    user = await users.get(id = user_id)
    update_info = update_info.dict(exclude_unset=True)
    user.name_user = update_info['name_user']
    user.email_user = update_info['email_user']
    if update_info['password'] is not None:
        if update_info['password'] == user.password:
            user.password = update_info['password']
        else: user.password = bcrypt.hash(update_info['password'])
    else: user.password = None
    user.photo = update_info['photo']
    user.date_registration = update_info['date_registration']
    user.date_lastAuth = update_info['date_lastAuth']
    user.status=update_info['status']
    user.bloking=update_info['bloking']
    user.confirmed=update_info['confirmed']
    await user.save()
    return await user_pydantic.from_tortoise_orm(user)


async def del_user(user_id: int):
    return await users.get(id=user_id).delete()

