from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()
url = os.getenv("DB_URL")

engine = create_engine(url)

sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()