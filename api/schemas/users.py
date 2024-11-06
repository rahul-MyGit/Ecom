from pydantic import BaseModel

class UserBase(BaseModel):
    name: str
    email: str
    password: str

class UserCreate(UserBase):
    pass

class UserEdit(UserBase):
    pass