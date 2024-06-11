from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator

#Status_message
class status_message(Model):
    id = fields.SmallIntField(pk=True)
    name_status = fields.CharField(max_length=150, null=False)

#create pydantic models Status_message
status_message_pydantic = pydantic_model_creator(status_message, name="status_message")