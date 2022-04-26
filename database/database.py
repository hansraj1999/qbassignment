from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sqlite3
import psycopg2

#SQLALCHAMY_DB_URL = 'sqlite:///database/data.db'
#engine = create_engine(SQLALCHAMY_DB_URL, connect_args={'check_same_thread': False})

#SQLALCHAMY_DB_URL = 'mysql+mysqlconnector://root:root@localhost:3306/qblocks'
#engine = create_engine(SQLALCHAMY_DB_URL)

# SQLALCHAMY_DB_URL = 'mysql+mysqlconnector://uvayh5ymlkx8ybfd:HJEYCKFKknzzlP7cvlKL@bjylablqdhnmt0gvpyai-mysql.services.clever-cloud.com:3306/bjylablqdhnmt0gvpyai'
# engine = create_engine(SQLALCHAMY_DB_URL)

SQLALCHEMY_DATABASE_URL = "postgresql://wzfjmqrbdydvjw:0c18a705fa8cd156f0d47b77ffca8130d5b3941e224771f3ed9cbeab23e3abb0@ec2-3-223-213-207.compute-1.amazonaws.com:5432/derqlf1da4p838"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
