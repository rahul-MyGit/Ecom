from fastapi import APIRouter, Request, HTTPException, Depends 
from typing import List
from schemas.auth import Signup, Login
from utils.generatetoken import create_access_token, get_hashed_password, verify_password
from models import User
from sqlalchemy.orm import Session
from utils.init_db import get_db
from schemas.response import ResponseModel

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
def signup(data: Signup, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    hashed_password = get_hashed_password(data.password)
    new_user = User(name=data.name, email=data.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return ResponseModel(
        data=new_user,
        message='User created succesfully'
    )

@AUTH_ROUTER.post('/login')
def login(data: Login, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    access_token = create_access_token(user.id)
    return {"access_token": access_token, "token_type": "bearer"}