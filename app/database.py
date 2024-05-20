
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker,scoped_session
from dotenv import load_dotenv
import os

load_dotenv()

# SQLALCHEMY_DATABASE_URL = "mysql://root:admin!123@local/cruddb"
# SQLALCHEMY_DATABASE_URL = "sqlite:///./todolistdb.sqlite"
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create SQLAlchemy engine
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:admin!123@localhost:3306/eventdb"


engine = create_engine(SQLALCHEMY_DATABASE_URL) 

# SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False,)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False,)
# SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

