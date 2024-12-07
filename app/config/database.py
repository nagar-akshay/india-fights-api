import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()


# Configure your production db
db_url = f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}"
db_name = os.getenv("DB_NAME")
db_username = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")

connectionString = f'mariadb+pymysql://{db_username}:{db_password}@{db_url}/{db_name}'

# use echo=True for debugging
engine = create_engine(connectionString, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def create_db_and_tables():
    Base.metadata.create_all(engine)
