from jose import JWTError, jwt
from datetime import datetime, timedelta
from schemas import TokenData
from fastapi import Depends,HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import get_db
from models import Users

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY  = '4f0b04f61d772f9400810476490d44bef63128c25951c929d59f18be9c3313e6'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440

def create_access_token(data: dict):
    to_encode = data.copy()
    # Add the expiration time to the token
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    # Encode the token
    encoded_jwt_token = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

    return encoded_jwt_token

def verify_access_token(token: str,credentials_exception):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        id: str =  payload.get('user_id')
        if id is None:
            raise credentials_exception
        token_data = TokenData(user_id=id)
    except JWTError:
        return None
    return token_data
    
def get_current_user(token:str= Depends(oauth2_scheme),db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=401,detail="Could not validate credentials",headers={"WWW-Authenticate":"Bearer"})

    token = verify_access_token(token,credentials_exception) 

    user = db.query(Users).filter(Users.id == token.user_id).first()

    return user
    