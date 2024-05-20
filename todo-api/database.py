
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker,scoped_session

# SQLALCHEMY_DATABASE_URL = "mysql://root:admin!123@local/cruddb"
# SQLALCHEMY_DATABASE_URL = "sqlite:///./todolistdb.sqlite"

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:admin!123@localhost:3306/todolistdb"
# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:root@localhost:3306/todo_db"

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

Base.metadata.create_all(bind=engine)