from fastapi import  status,HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from database import get_db
import models
from schemas import CreatePost, UpdatePost

router = APIRouter(
    prefix="/sqlalchemy/posts",
    tags=['Posts']
)

@router.get('/',response_model=list[UpdatePost])
async def get_sqlalchemy_posts(db: Session = Depends(get_db)):

    posts =  db.query(models.Post).all()
    return posts
    

@router.post('/sqlalchemy/post',status_code=status.HTTP_201_CREATED,response_model=UpdatePost)
async def create_sqlalchemy_post(post: CreatePost, db: Session = Depends(get_db)):

    new_post = models.Post(**post.dict())
    db.add(new_post) 
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get('/{id}')
async def get_sqlalchemy_post (id:int, db:Session= Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post:
        return post 
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} was not found")

@router.delete('/{id}', status_code=status.HTTP_200_OK)
async def delete_sqlalchemy_post(id:int, db:Session=Depends(get_db)):
   
   deleted_post = db.query(models.Post).filter(models.Post.id == id)
   if deleted_post.first() == None: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} was not found")
   deleted_post.delete(synchronize_session=False)
   db.commit()
   return {"message": f"Post with id {id} was deleted successfully"}

@router.put('/{id}')
async def update (id:int,post:CreatePost, db:Session=Depends(get_db)):
   
   post_to_be_updated = db.query(models.Post).filter(models.Post.id == id)
   if post_to_be_updated.first() == None: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} was not found")
   post_to_be_updated.update(post.dict() ,synchronize_session=False)
   db.commit()
   return {"message": f"Post with id {id} was updated successfully",
            "updated_post":post_to_be_updated.first()}
