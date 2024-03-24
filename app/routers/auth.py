from fastapi import  status,HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
from schemas import Token
from models import Users
from utils import verify_password
from oauth2 import create_access_token

router = APIRouter(tags=['Authentication'])

@router.post('/login',response_model=Token)
# This is the old way of doing it
# Using this we need to send the data in the body of the request
# def login(user_credentials:UserLoginSchema,db: Session = Depends(get_db)):

# This is the new way of doing it
# Using this we can send the data in the form of form-data
def login(user_credentials:OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid Credentials")

    verification = verify_password(user_credentials.password,user.password)
    if not verification:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid Credentials")
    
    # Create a new token for the user
    access_taken = create_access_token(data={"user_id":user.id})

    return {"access_token":access_taken,"token_type":"bearer"}
