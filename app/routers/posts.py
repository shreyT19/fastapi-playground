from fastapi import  status,HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from database import get_db
import models
from schemas import CreatePost, UpdatePost
from oauth2 import get_current_user

router = APIRouter(
    prefix="/sqlalchemy/posts",
    tags=['Posts']
)

@router.get('/',response_model=list[UpdatePost])
async def get_sqlalchemy_posts(db: Session = Depends(get_db),current_user:int = Depends(get_current_user)):

    posts =  db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    return posts
    

@router.post('/',status_code=status.HTTP_201_CREATED,response_model=UpdatePost)
async def create_sqlalchemy_post(post: CreatePost, db: Session = Depends(get_db),current_user:int = Depends(get_current_user)):
    # adding the owner_id to the post object
    new_post = models.Post(owner_id = current_user.id,**post.dict())
    db.add(new_post) 
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get('/{id}')
async def get_sqlalchemy_post(id:int, db:Session= Depends(get_db),current_user:int = Depends(get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post is None: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} was not found")
    if(post.owner_id != current_user.id): raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"User with id {current_user.id} is not authorized to view post with id {id}")
    return post 
    

@router.delete('/{id}', status_code=status.HTTP_200_OK)
async def delete_sqlalchemy_post(id:int, db:Session=Depends(get_db),current_user:int = Depends(get_current_user)):
   
   deleted_post_query = db.query(models.Post).filter(models.Post.id == id)
   deleted_post = deleted_post_query.first()
   if deleted_post == None: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} was not found")
   if(deleted_post.owner_id != current_user.id): raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"User with id {current_user.id} is not authorized to delete post with id {id}")
   deleted_post_query.delete(synchronize_session=False)
   db.commit()
   return {"message": f"Post with id {id} was deleted successfully"}

@router.put('/{id}')
async def update (id:int,updated_post:CreatePost, db:Session=Depends(get_db),current_user:int = Depends(get_current_user)):
   
   post_query = db.query(models.Post).filter(models.Post.id == id)
   post = post_query.first()
   
   if post == None: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} was not found")
   if(post.owner_id != current_user.id): raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"User with id {current_user.id} is not authorized to update post with id {id}")
   post_query.update(updated_post.dict() ,synchronize_session=False)
   db.commit()
   return {"message": f"Post with id {id} was updated successfully",
            "updated_post":post_query.first()}
