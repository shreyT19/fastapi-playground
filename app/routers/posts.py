from fastapi import  status,HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
import models
from schemas import CreatePost, UpdatePost, PostOut
from oauth2 import get_current_user
from typing import Optional
from pydantic import ValidationError

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


# @router.get('/')
# @router.get('/',response_model=list[UpdatePost])
@router.get('/',response_model=list[PostOut])
async def get_sqlalchemy_posts(db: Session = Depends(get_db),current_user:int = Depends(get_current_user),limit:int=10,skip:int=0, searchQuery: Optional[str] = ''):

    #here "skip" skips the first "skip" number of posts 
    #suppose we have 10 posts and we want to skip the first 5 posts and get the next 5 posts
    #we will set skip = 5
    # posts =  db.query(models.Post).filter(models.Post.owner_id == current_user.id)
    # posts = posts.filter(func.lower(models.Post.title).contains(searchQuery.lower())).offset(skip).limit(limit).all()
    
    
    #isouter=True is used to get all the posts even if there are no votes for the post
    try:
        results = db.query(models.Post,func.count(models.Votes.post_id).label('votes'))\
                    .join(models.Votes,models.Post.id == models.Votes.post_id,isouter=True)\
                    .group_by(models.Post.id).all()
        print(results)
        
    except ValidationError as e:
        print(repr(e.errors()[0]['type']))
    
    # Return the list of dictionaries
    return results
    # return []
    

@router.post('/',status_code=status.HTTP_201_CREATED,response_model=UpdatePost)
async def create_sqlalchemy_post(post: CreatePost, db: Session = Depends(get_db),current_user:int = Depends(get_current_user)):
    # adding the owner_id to the post object
    new_post = models.Post(owner_id = current_user.id,**post.dict())
    db.add(new_post) 
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get('/{id}',response_model=PostOut)
async def get_sqlalchemy_post(id:int, db:Session= Depends(get_db),current_user:int = Depends(get_current_user)):

    # post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post,func.count(models.Votes.post_id).label('votes'))\
                    .join(models.Votes,models.Post.id == models.Votes.post_id,isouter=True)\
                    .group_by(models.Post.id).first()
    if post is None: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} was not found")
    if(post.Post.owner_id != current_user.id): raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"User with id {current_user.id} is not authorized to view post with id {id}")
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
