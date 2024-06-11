from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator

#Chats
class chats(Model):
    id = fields.SmallIntField(pk=True)
    chat_name = fields.CharField(max_length=150, null=False)
    date_creating = fields.DatetimeField(null=False)
    user = fields.ForeignKeyField('models.users', related_name='user_id', to_field = 'id', null=False)
    type_nn = fields.ForeignKeyField('models.type_nn', to_field = 'id', null=False)
    date_deleting = fields.DatetimeField(null=True)
    deleting = fields.BooleanField(null=False)

#create pydantic models Chats
chats_pydantic = pydantic_model_creator(chats, name="chats")
chats_pydanticIN = pydantic_model_creator(chats, name="chatsIn", exclude_readonly=True)