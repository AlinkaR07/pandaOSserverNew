from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator
from passlib.hash import bcrypt


#Users
class users(Model):
    id = fields.SmallIntField(pk=True)
    name_user = fields.CharField(max_length=150, null=False)
    password = fields.CharField(max_length=150, null=True)
    email_user = fields.CharField(max_length=255, null=False)
    photo = fields.CharField(max_length=300, null=True)
    date_registration = fields.DateField(null=False)
    date_lastAuth = fields.DateField(null=True)
    status = fields.CharField(max_length=255, null=False)
    bloking = fields.BooleanField(null=False)
    confirmed = fields.BooleanField(null=False)

    def verify_password(self, password_user):
        return bcrypt.verify(password_user, self.password)
    
#create pydantic models Users
user_pydantic = pydantic_model_creator(users, name="users")
user_pydanticIN = pydantic_model_creator(users, name="usersIn", exclude_readonly=True)