# run in terminal: uvicorn app.main:app --reload

from typing import List
from fastapi import Body, FastAPI, Depends
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models #import from current dir
from .database import engine, get_db
from .routers import post, user, auth, vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

# create tables using SQLalchemy
# models.Base.metadata.create_all(bind=engine) # NO LONGER NEEDED AFTER USING ALEMBIC

app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)
print(settings)

# from FASTAPI Documentation:

# while True:
#     try: # best to use try-except in case it fails
#         conn = psycopg2.connect(host = 'localhost', database = 'fastapi',
#                                 user = 'postgres', password='Galactica91', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print('Database connection was successful!')
#         break
#     except Exception as error:
#         print("Connecting to database failed")
#         print("Error:", error)
#         time.sleep(2)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message":"Hello world!"}