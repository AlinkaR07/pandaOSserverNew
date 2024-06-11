from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator

#Type_NN
class type_nn(Model):
    id = fields.SmallIntField(pk=True)
    name_nn = fields.CharField(max_length=200, null=False)

#create pydantic models Type_NN
type_nn_pydantic = pydantic_model_creator(type_nn, name="type_nn")
#type_nn_pydanticIN = pydantic_model_creator(type_nn, name="type_nnIn", exclude_readonly=True)