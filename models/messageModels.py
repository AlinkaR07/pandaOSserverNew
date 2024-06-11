from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator

#Messages
class messages(Model):
    id = fields.SmallIntField(pk=True)
    content = fields.TextField(null=True)
    status_message = fields.ForeignKeyField('models.status_message', to_field = 'id', null=False)
    user = fields.ForeignKeyField('models.users', to_field = 'id', null=False)
    chat = fields.ForeignKeyField('models.chats', to_field = 'id', null=False)
    date_sending = fields.DatetimeField(null=True)

    
#create pydantic models Messages
messages_pydantic = pydantic_model_creator(messages, name="messages", include=("id", "content", "date_sending", "status_message"))
messages_pydanticIN = pydantic_model_creator(messages, name="messagesIn", exclude_readonly=True)


