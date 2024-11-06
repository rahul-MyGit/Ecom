from typing import Dict
from schemas.users import User
from fastapi import APIRouter

users_db: Dict[int, User] = {}

USER_ROUTER = APIRouter()


@USER_ROUTER.get('/')
def get_users():
    return list(users_db)

@USER_ROUTER.post('/', response_model=User)
def create_user(user: User):
    for id, user_data in users_db.items():
        if user.username == user_data.username:
            return "nahhh"
    user_id = len(users_db) + 1
    users_db[user_id] = user
    print(users_db)
    return user



@USER_ROUTER.get('/name/{name}')
def get_user_id(name: str):
    print(name)
    userdetails = []
    for id, user_data in users_db.items():
        if name == user_data.username:
            userdetails.append(user_data)
        
    
    return userdetails

