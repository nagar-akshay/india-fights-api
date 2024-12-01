from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# Configure your production db
db_username = "root"
db_password = "admin123"
db_url = "127.0.0.1:3306"
db_name = "ifapi"

connectionString = f'mariadb+pymysql://{db_username}:{db_password}@{db_url}/{db_name}'

# use echo=True for debugging
engine = create_engine(connectionString, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def create_db_and_tables():
    Base.metadata.create_all(engine)
