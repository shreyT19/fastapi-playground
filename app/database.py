from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings

# SQLALCHEMY_DATABASE_URL = "postgresql://<username>:<password>@<ip-address/host-name>/<database_name>"
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/postgres"
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

# Create the SQLAlchemy engine
#responsible for the connection to the database
engine = create_engine(SQLALCHEMY_DATABASE_URL) 

# Create a session class
# This is the main handle to the database
# The session class is a factory for making session objects
# It is not a session itself
# The session object is the handle to the database

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class
# This is the class that our models will inherit from
# This class will be used to create our models
Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



