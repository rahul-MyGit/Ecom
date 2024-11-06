
from fastapi import APIRouter, Depends, Request
from schemas.users import User
from sqlalchemy.orm import Session
from utils.init_db import get_db
from config.db import ItemRepo

# from . import models

ITEM_ROUTER = APIRouter()

@ITEM_ROUTER.get('/')
async def get_all_items(db: Session = Depends(get_db)):
    res = await ItemRepo.fetchAll(db)
    return res

@ITEM_ROUTER.post('/', response_model=User)
async def create_items(request: Request, db: Session = Depends(get_db)):
    res = await ItemRepo.create(db, request.body)
    return res


