from fastapi import FastAPI, Response, status,HTTPException, Depends
import psycopg2
from psycopg2.extras import RealDictCursor
import time
import models
from sqlalchemy.orm import Session
from database import engine,get_db
from schemas import CreatePost

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


while True:
    try:
        connection = psycopg2.connect(
            host="localhost",
            database="postgres",
            user="postgres",
            password="postgres",
            cursor_factory=RealDictCursor
        )
        cursor = connection.cursor()
        print("Connection to the database was successful")
        break
    except Exception as e:
        print("Connection to the database was not successful")
        print("Error",e)
        time.sleep(5)



@app.get('/sqlalchemy/posts')
async def get_sqlalchemy_posts(db: Session = Depends(get_db)):
    posts =  db.query(models.Post).all()
    return {"data": posts}
    

@app.post('/sqlalchemy/post',status_code=status.HTTP_201_CREATED)
async def create_sqlalchemy_post(post: CreatePost, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post) 
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}

@app.get('/sqlalchemy/posts/{id}')
async def get_sqlalchemy_post (id:int, db:Session= Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post:
        return {"post_details":post}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} was not found")

@app.delete('/sqlalchemy/posts/{id}', status_code=status.HTTP_200_OK)
async def delete_sqlalchemy_post(id:int, db:Session=Depends(get_db)):
   
   deleted_post = db.query(models.Post).filter(models.Post.id == id)
   if deleted_post.first() == None: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} was not found")
   deleted_post.delete(synchronize_session=False)
   db.commit()
   return {"message": f"Post with id {id} was deleted successfully"}

@app.put('/sqlalchemy/posts/{id}')
async def update (id:int,post:CreatePost, db:Session=Depends(get_db)):
   post_to_be_updated = db.query(models.Post).filter(models.Post.id == id)
   if post_to_be_updated.first() == None: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} was not found")
   post_to_be_updated.update(post.dict() ,synchronize_session=False)
   db.commit()
   return {"message": f"Post with id {id} was updated successfully",
            "updated_post":post_to_be_updated.first()}
