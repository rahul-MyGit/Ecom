from jwt.exceptions import InvalidTokenError
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import jwt
from schemas.response import ErrorResponseModel
from utils.init_db import SessionLocal
from models import User

ALGORITHM='HS256'
SECRET_KEY = 'asdasujikdnASLOIFGNADFSIULVNSaeliFG'

class AuthMiddleware(BaseHTTPMiddleware):
    async def verify_token(self, request: Request):
        try:
            token = request.headers.get('Authorization')
            if token:
                payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
                user_id =  payload.get('user_id')

                db = SessionLocal()
                user = db.query(User).filter(User.id == user_id).first()
                request.state.user =  user
        except InvalidTokenError:
            return ErrorResponseModel("Invalid token", 201, "Unautorized")