from pydantic import BaseModel, EmailStr
from typing import Optional


# свойства, необходимые при создании пользователя.
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


a = UserCreate
a.username = 'dsd'
print(a.username)
a.username = 1
print(type(a.username))

a.email = 1111
print(a.email)