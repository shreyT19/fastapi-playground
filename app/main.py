from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
import time
import models
from database import engine
from routers import posts, users, auth
from config import settings
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


app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
