# from typing import Dict
# from schemas.users import User
# from fastapi import APIRouter

# users_db: Dict[int, User] = {}

# USER_ROUTER = APIRouter()


# @USER_ROUTER.get('/')
# def get_users():
#     return list(users_db)

# @USER_ROUTER.post('/', response_model=User)
# def create_user(user: User):
#     for id, user_data in users_db.items():
#         if user.username == user_data.username:
#             return "nahhh"
#     user_id = len(users_db) + 1
#     users_db[user_id] = user
#     print(users_db)
#     return user



# @USER_ROUTER.get('/name/{name}')
# def get_user_id(name: str):
#     print(name)
#     userdetails = []
#     for id, user_data in users_db.items():
#         if name == user_data.username:
#             userdetails.append(user_data)
        
    
#     return userdetails

print('hhhhhhhhhhhhhhhhhhhhhhoooooooooooooooooooooooooooooooooooeeeeeeeeeeeeeeeeeeeeeeeeeeee')

from fastapi import APIRouter, Depends, Request, HTTPException
from schemas.users import UserCreate
from sqlalchemy.orm import Session
from utils.init_db import get_db
from config.db import UserRepo
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, update
from models.dbModel import Item, User
from middleware.protectRoute import verify_token

USER_ROUTER = APIRouter()

@USER_ROUTER.get('/')
async def get_all_users(db: Session = Depends(get_db)):
    res = db.query(User).all()
    return res

@USER_ROUTER.post('/', response_model=UserCreate)
async def create_user(request: Request, db: Session = Depends(get_db)):
    res = await UserRepo.create(db, request.body)
    return res


@USER_ROUTER.post("/{item_id}", dependencies=[Depends(verify_token)])
def buy_item(item_id: int, quantity: int, db: Session = Depends(get_db), request: Request = None):
    if not request.state.user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    er = request.state.user
    
    with db.begin_nested():
        item = db.execute(select(Item).where(Item.id == item_id).with_for_update()).scalar_one_or_none()
        
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        if item.quantity < quantity:
            raise HTTPException(status_code=400, detail="Insufficient stock")

        new_quantity = item.quantity - quantity
        if new_quantity < 0:
            raise HTTPException(status_code=400, detail="Not enough items in stock")

        db.execute(
            update(Item)
            .where(Item.id == item_id)
            .values(quantity=new_quantity)
        )

    try:
        db.commit()
        return {"msg": "Purchase successful", "remaining_quantity": new_quantity}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Transaction error")
