from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
from psycopg2.extras import RealDictCursor
import time
import models
from database import engine
from routers import posts, users, auth, votes
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

ALLOWED_HOSTS = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)
