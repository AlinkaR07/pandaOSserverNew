from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator

#Chats
class alerts(Model):
    id = fields.SmallIntField(pk=True)
    date_sending = fields.DatetimeField(null=False)
    user = fields.ForeignKeyField('models.users', related_name='alerts', to_field = 'id', null=False)
    reading = fields.BooleanField(null=False)

#create pydantic models Chats
alerts_pydantic = pydantic_model_creator(alerts, name="alerts")
alerts_pydanticIN = pydantic_model_creator(alerts, name="alertsIn", exclude_readonly=True)