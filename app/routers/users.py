from fastapi import  status,HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from database import get_db
import models
from schemas import UserCreate, UserResponseSchema
from utils import get_password_hash

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.post('/',status_code=status.HTTP_201_CREATED,response_model=UserResponseSchema)
async def create_user(user: UserCreate,db: Session = Depends(get_db)):

    # we are hashing the password before storing it in the database
    hashed_password = get_password_hash(user.password)
    user.password = hashed_password
    new_user = models.Users(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/{id}',response_model=UserResponseSchema)
async def get_user(id:int,db: Session = Depends(get_db)):

    user = db.query(models.Users).filter(models.Users.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} was not found")
    return user