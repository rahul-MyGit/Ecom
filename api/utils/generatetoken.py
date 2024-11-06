import jwt
from pydantic import BaseModel
from passlib.context import CryptContext


password_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

def get_hashed_password(passsword: str) -> str:
    return password_context.hash(passsword)

def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password,hashed_pass)

# TODO: Remove later to .env
SECRET_KEY = 'asdasujikdnASLOIFGNADFSIULVNSaeliFG'
ALGORITHM = "HS256"
# adminapikey = "hahahehehahahehe"

class Token(BaseModel):
    access_token:str
    token_type:str


def create_access_token(user_id: int) -> str:
    to_encode = {"user_id": user_id}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt