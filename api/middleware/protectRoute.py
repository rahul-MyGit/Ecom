from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
from fastapi import Request, Depends, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
import jwt
from schemas.response import ErrorResponseModel
from models import User
from sqlalchemy.orm import Session
from utils.init_db import get_db
# import os
# os.getenv()

ALGORITHM = 'HS256'
SECRET_KEY = 'asdasujikdnASLOIFGNADFSIULVNSaeliFG'

async def verify_token(request: Request, db: Session = Depends(get_db)):
    token = request.headers.get('Authorization')
    if token:
        try:
            token = token.replace("Bearer ", "")
            payload = jwt.verify(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id = payload.get('user_id')

            user = db.query(User).filter(User.id == user_id).first()

            if user is None:
                raise HTTPException(status_code=403, detail="User not found")

            request.state.user = user
        except InvalidTokenError:
            raise HTTPException(status_code=403, detail="Invalid token")
        except:
            raise HTTPException(status_code=403, detail="Error verifying token")
    else:
        raise HTTPException(status_code=403, detail="Authorization token not provided")

    return request.state.user

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            await verify_token(request)
        except HTTPException as e:
            return ErrorResponseModel(e.detail, e.status_code, "Unauthorized")

        response = await call_next(request)
        return response