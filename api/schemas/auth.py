from pydantic import BaseModel

class Auth(BaseModel):
    username: str
    password: str

class Login(BaseModel):
    pass

class Signup(Auth):
    name: str
    age: int