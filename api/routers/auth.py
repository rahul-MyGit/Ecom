from fastapi import APIRouter, Request
from typing import List
from schemas.auth import Signup

allUsers : List[Signup] = []

AUTH_ROUTER= APIRouter()

@AUTH_ROUTER.get('/me')
def get_me(request: Request):
    name = request.args.get('name')
    for user in allUsers:
        if user.username == name:
            return user
    return {'message': 'Not Found'}


@AUTH_ROUTER.post('/signup')
def signup(data: Signup):
    for user in allUsers:
        if user.username == data.username & user.password == data.passwrod:
            return {"message": 'User exist prev'}
    allUsers.append(data)
    print(allUsers)
    return {"message": "User created successfully"}