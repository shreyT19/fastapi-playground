from fastapi import FastAPI, Response, status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time


app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool=True
    rating:Optional[int] = None

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

my_posts = [{
    "id": 1,
    "title": "Post 1",
    "description": "This is post 1",
    "published": True,
    "rating": 4
},
{
    "id": 2,
    "title": "Post 2",
    "description": "This is post 2",
    "published": True,
    "rating": 3
},
{
    "id": 3,
    "title": "Post 3",
    "description": "This is post 3",
    "published": False,
    "rating": 5

},
{
    "id": 4,
    "title": "Post 4",
    "description": "This is post 4",
    "published": True,
    "rating": 2
}
]

@app.get("/")
async def root():
    return {"message": "Welcome to the API response"}


@app.get('/posts')
async def get_posts():
    cursor.execute("""SELECT * FROM posts;""")
    database_posts = cursor.fetchall()
    return {"data": database_posts}


@app.post('/posts',status_code=status.HTTP_201_CREATED)
async def create_post(post: Post):
    cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING *;""",(post.title,post.content,post.published))

    database_post = cursor.fetchone()
    print(database_post, 'database post')
    connection.commit()
    if not database_post:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Post was not created")

    return {"data": database_post}


@app.get('/posts/{id}')
async def get_post(id:int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    post = cursor.fetchone()
    if post:
        return {"post_details":post}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} was not found")
  

@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id:int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    deleted_post = cursor.fetchone()
    connection.commit()
    print(deleted_post, 'deleted post')
    if deleted_post:
        return {"message": f"Post with id {id} was deleted successfully",
                "deleted_post":deleted_post}
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} was not found")
    

@app.put('/posts/{id}')
async def update_post(id:int,post:Post):

    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *;""",(post.title,post.content,post.published,str(id)))
    updated_post = cursor.fetchone()
    connection.commit()
    if updated_post:
        return {"message": f"Post with id {id} was updated successfully",
                "updated_post":updated_post}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} was not found")