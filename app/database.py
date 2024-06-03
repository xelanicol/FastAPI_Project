# see sqlalchemy Documentation to explain the following code:
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:password@localhost/fastapi'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # default values

Base = declarative_base() # base class for database tables

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()